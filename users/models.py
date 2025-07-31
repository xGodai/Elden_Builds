from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50, blank=True, help_text="Display name (optional, defaults to username)")
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    location = models.CharField(max_length=100, blank=True, help_text="Your location")
    favorite_weapon = models.CharField(max_length=100, blank=True, help_text="Your favorite Elden Ring weapon")
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

    def get_profile_picture_url(self):
        """Return profile picture URL or a default placeholder"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            # Return a placeholder image URL
            return f"https://ui-avatars.com/api/?name={self.get_display_name()}&background=6c757d&color=ffffff&size=300"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it exists and is too large
        if self.profile_picture and hasattr(self.profile_picture, 'path'):
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except Exception:
                # If PIL fails or file doesn't exist, continue silently
                pass

    def total_builds(self):
        return self.user.build_set.count()

    def total_liked_builds(self):
        return self.user.liked_builds.count()

    def total_comments(self):
        return self.user.comment_set.count()
