from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import cloudinary.uploader

# Create your models here.

def validate_image_size(value):
    """Validate that the uploaded image doesn't exceed 10MB"""
    if value and hasattr(value, 'size'):
        if value.size > 10 * 1024 * 1024:  # 10MB in bytes
            raise ValidationError('Image file too large. Maximum size is 10MB.')
    return value

class Build(models.Model):

    CATEGORY_CHOICES = [
        ('PVE', 'PvE'),
        ('PVP', 'PvP'),
        ('BOTH', 'Both'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    weapons = models.CharField(max_length=100)
    armor = models.CharField(max_length=100)
    talismans = models.CharField(max_length=100)
    spells = models.CharField(max_length=100, blank=True, null=True)
    # Remove single image field - we'll use BuildImage model instead
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='PVE')
    liked_by = models.ManyToManyField(User, related_name='liked_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.liked_by.count()
    
    def get_primary_image(self):
        """Get the primary (first) image for this build"""
        primary_image = self.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = self.images.first()
        return primary_image
    
    def get_image_url(self, size='medium'):
        """Return optimized build image URL or default image"""
        primary_image = self.get_primary_image()
        if primary_image:
            from utils.cloudinary_utils import get_build_image_url, get_thumbnail_url, BUILD_SIZES
            if size == 'thumbnail':
                return get_thumbnail_url(primary_image.image)
            else:
                size_config = BUILD_SIZES.get(size, BUILD_SIZES['medium'])
                return get_build_image_url(primary_image.image, size_config['width'], size_config['height'])
        return None  # Will use CSS default image
    
    def has_custom_image(self):
        """Check if build has any uploaded images"""
        return self.images.exists()
    
    def can_add_image(self):
        """Check if build can have more images (max 3)"""
        return self.images.count() < 3

    def get_absolute_url(self):
        return reverse('build-detail', kwargs={'pk': self.pk})


class BuildImage(models.Model):
    """Model for storing multiple images per build (max 3)"""
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField(
        'image', 
        folder='build_images/',
        validators=[validate_image_size],
        transformation={
            'quality': 'auto:good',
            'fetch_format': 'auto',
            'width': 1200,
            'height': 800,
            'crop': 'limit'
        }
    )
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def save(self, *args, **kwargs):
        # Validate max 3 images per build
        if not self.pk and self.build.images.count() >= 3:
            raise ValidationError('Maximum 3 images allowed per build.')
        
        # If this is the first image for the build, make it primary
        if not self.pk and not self.build.images.exists():
            self.is_primary = True
        
        # If setting as primary, remove primary status from other images
        if self.is_primary:
            BuildImage.objects.filter(build=self.build, is_primary=True).update(is_primary=False)
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # If deleting primary image, make the next image primary
        if self.is_primary and self.build.images.count() > 1:
            next_image = self.build.images.exclude(pk=self.pk).first()
            if next_image:
                next_image.is_primary = True
                next_image.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.build.title} {'(Primary)' if self.is_primary else ''}"


class Comment(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.build.title}'

    def get_absolute_url(self):
        return reverse('build-detail', kwargs={'pk': self.build.pk})

    def total_upvotes(self):
        return self.votes.filter(vote_type='upvote').count()

    def total_downvotes(self):
        return self.votes.filter(vote_type='downvote').count()

    def vote_score(self):
        return self.total_upvotes() - self.total_downvotes()

    def user_vote(self, user):
        """Get the current user's vote on this comment"""
        if not user.is_authenticated:
            return None
        try:
            return self.votes.get(user=user).vote_type
        except CommentVote.DoesNotExist:
            return None


class CommentVote(models.Model):
    VOTE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']  # One vote per user per comment

    def __str__(self):
        return f'{self.user.username} {self.vote_type}d comment by {self.comment.user.username}'
