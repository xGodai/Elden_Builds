from django.urls import path
from . import views
from .views import UserProfileView
from . import notification_views

urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path(
        'profile/<str:username>/',
        UserProfileView.as_view(),
        name='user-profile'),

    # Notification URLs
    path(
        'notifications/',
        notification_views.notification_list,
        name='notification-list'),
    path(
        'notifications/mark-read/<int:notification_id>/',
        notification_views.mark_notification_read,
        name='mark-notification-read'),
    path(
        'notifications/mark-read/',
        notification_views.mark_notifications_read,
        name='notification-mark-read'),
    path('notifications/mark-all-read/',
         notification_views.mark_all_notifications_read,
         name='mark-all-notifications-read'),
    path(
        'notifications/delete/<int:notification_id>/',
        notification_views.delete_notification,
        name='delete-notification'),
    path('notifications/unread-count/',
         notification_views.get_unread_count,
         name='unread-notification-count'),
]
