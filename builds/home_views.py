from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import models
from .models import Build, Comment


def home(request):
    """Home page view with statistics and featured content"""
    context = {
        'total_builds': Build.objects.count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
        'recent_builds': Build.objects.select_related('user').order_by('-created_at')[:3],
        'popular_builds': Build.objects.select_related('user').annotate(
            like_count=models.Count('liked_by')
        ).order_by('-like_count')[:3] if Build.objects.exists() else [],
    }
    return render(request, 'builds/home.html', context)
