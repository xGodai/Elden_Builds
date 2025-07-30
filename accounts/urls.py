from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),    # use login_view here
    path('logout/', views.logout_view, name='logout'), # use logout_view here
]
