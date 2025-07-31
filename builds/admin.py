from django.contrib import admin
from .models import Build, BuildImage, Comment, CommentVote

# Register your models here.

class BuildImageInline(admin.TabularInline):
    model = BuildImage
    extra = 1
    max_num = 3
    fields = ['image', 'is_primary', 'caption']

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'created_at', 'total_likes', 'image_count']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'user__username']
    inlines = [BuildImageInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'

@admin.register(BuildImage)
class BuildImageAdmin(admin.ModelAdmin):
    list_display = ['build', 'is_primary', 'caption', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['build__title', 'caption']

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