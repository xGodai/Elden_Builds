from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    image = models.ImageField(upload_to='build_images/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='PVE')
    liked_by = models.ManyToManyField(User, related_name='liked_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.liked_by.count()

    def get_absolute_url(self):
        return reverse('build-detail', kwargs={'pk': self.pk})
