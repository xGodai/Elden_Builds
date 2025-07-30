from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Build(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    weapons = models.CharField(max_length=100)
    armor = models.CharField(max_length=100)
    talismans = models.CharField(max_length=100)
    spells = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='build_images/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
