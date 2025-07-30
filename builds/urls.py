from django.urls import path
from . import views
from .views import (
    BuildListView,
    BuildDetailView,
    BuildCreateView,
    BuildUpdateView,
    BuildDeleteView,
)

urlpatterns = [
    path('', BuildListView.as_view(), name='build-list'),
    path('build/<int:pk>/', BuildDetailView.as_view(), name='build-detail'),
    path('build/new/', BuildCreateView.as_view(), name='build-create'),
    path('build/<int:pk>/edit/', BuildUpdateView.as_view(), name='build-update'),
    path('build/<int:pk>/delete/', BuildDeleteView.as_view(), name='build-delete'),
    path('build/<int:pk>/like/', views.like_build, name='build-like'),
]
