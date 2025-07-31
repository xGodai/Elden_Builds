from django.urls import path
from . import views
from .views import UserProfileView

urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
]
