from django.contrib import admin
from .models import Build, Comment, CommentVote

# Register your models here.

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'created_at', 'total_likes']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'user__username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'build', 'vote_score', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'build__title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'comment__content']