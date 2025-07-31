from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

# Create your models here.

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
    image = CloudinaryField('image', blank=True, null=True, folder='build_images/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='PVE')
    liked_by = models.ManyToManyField(User, related_name='liked_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.liked_by.count()
    
    def get_image_url(self, size='medium'):
        """Return optimized build image URL"""
        if self.image:
            from utils.cloudinary_utils import get_build_image_url, get_thumbnail_url, BUILD_SIZES
            if size == 'thumbnail':
                return get_thumbnail_url(self.image)
            else:
                size_config = BUILD_SIZES.get(size, BUILD_SIZES['medium'])
                return get_build_image_url(self.image, size_config['width'], size_config['height'])
        return None

    def get_absolute_url(self):
        return reverse('build-detail', kwargs={'pk': self.pk})


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
