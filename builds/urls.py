from django.urls import path
from . import views
from .home_views import home
from .views import (
    BuildListView,
    BuildDetailView,
    BuildCreateView,
    BuildUpdateView,
    BuildDeleteView,
    BuildLikeView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CommentVoteView,
)

urlpatterns = [
    path('', home, name='home'),
    path('builds/', BuildListView.as_view(), name='build-list'),
    path('build/<int:pk>/', BuildDetailView.as_view(), name='build-detail'),
    path('build/new/', BuildCreateView.as_view(), name='build-create'),
    path('build/<int:pk>/edit/', BuildUpdateView.as_view(), name='build-update'),
    path('build/<int:pk>/delete/', BuildDeleteView.as_view(), name='build-delete'),
    path('build/<int:pk>/like/', BuildLikeView.as_view(), name='build-like'),
    path('build/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/vote/<str:vote_type>/', CommentVoteView.as_view(), name='comment-vote'),
]
