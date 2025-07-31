from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['display_name', 'bio', 'profile_picture', 'location', 'favorite_weapon']

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_total_builds')
    
    def get_total_builds(self, obj):
        return obj.build_set.count()
    get_total_builds.short_description = 'Total Builds'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'location', 'favorite_weapon', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'display_name', 'location', 'favorite_weapon']
    readonly_fields = ['created_at', 'updated_at']
