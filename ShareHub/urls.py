from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    LikeView,
    CommentsView,
)

urlpatterns = [
    path('posts/', PostCreateView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikeView.as_view(), name='like-post'),
    path('posts/comments/', CommentsView.as_view(), name='post-comments'),
    path('posts/comments/<int:comments_id>/', CommentsView.as_view(), name='comment-detail'),
]