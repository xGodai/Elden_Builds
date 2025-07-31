from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
import hashlib

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50, blank=True, help_text="Display name (optional, defaults to username)")
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    profile_picture = CloudinaryField(
        'image', 
        blank=True,
        null=True,
        folder='profile_pics/',
        help_text="Profile picture"
    )
    location = models.CharField(max_length=100, blank=True, help_text="Your location")
    favorite_weapon = models.CharField(max_length=100, blank=True, help_text="Your favorite Elden Ring weapon")
    
    # Notification preferences
    notify_on_build_like = models.BooleanField(default=True, help_text="Receive notifications when someone likes your build")
    notify_on_build_comment = models.BooleanField(default=True, help_text="Receive notifications when someone comments on your build")
    notify_on_comment_reply = models.BooleanField(default=True, help_text="Receive notifications when someone replies to your comment")
    notify_on_comment_vote = models.BooleanField(default=False, help_text="Receive notifications when someone votes on your comment")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'username': self.user.username})

    def get_display_name(self):
        """Return display name if set, otherwise return username"""
        return self.display_name if self.display_name else self.user.username

    def get_profile_picture_url(self):
        """Return profile picture URL or default avatar"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            # Return a default avatar using a service like Gravatar or a placeholder
            import hashlib
            email_hash = hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest()
            return f"https://www.gravatar.com/avatar/{email_hash}?s=150&d=identicon"

    def get_profile_picture_url(self, size='medium'):
        """Return optimized profile picture URL or a default placeholder"""
        if self.profile_picture:
            from utils.cloudinary_utils import get_profile_picture_url, PROFILE_SIZES
            size_config = PROFILE_SIZES.get(size, PROFILE_SIZES['medium'])
            return get_profile_picture_url(self.profile_picture, size_config['width'])
        else:
            # Return a placeholder image URL  
            from utils.cloudinary_utils import PROFILE_SIZES
            size_px = PROFILE_SIZES.get(size, PROFILE_SIZES['medium'])['width']
            return f"https://ui-avatars.com/api/?name={self.get_display_name()}&background=6c757d&color=ffffff&size={size_px}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Cloudinary handles image optimization automatically
        # No need for manual image processing

    def total_builds(self):
        return self.user.build_set.count()

    def total_liked_builds(self):
        return self.user.liked_builds.count()

    def total_comments(self):
        return self.user.comment_set.count()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('build_like', 'Build Like'),
        ('build_comment', 'Build Comment'),
        ('comment_reply', 'Comment Reply'),
        ('comment_vote', 'Comment Vote'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Generic fields for different notification types
    build = models.ForeignKey('builds.Build', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('builds.Comment', on_delete=models.CASCADE, null=True, blank=True)
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:50]}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def get_absolute_url(self):
        """Return the URL this notification links to"""
        if self.build:
            return self.build.get_absolute_url()
        elif self.comment:
            return self.comment.build.get_absolute_url()
        return '#'
