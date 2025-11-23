from django.contrib import admin
from .models import PostCreate, Like, Comment

@admin.register(PostCreate)
class PostCreateAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_by', 'created_at')
    search_fields = ('text', 'created_by__username')
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'like_post', 'user')
    search_fields = ('user__username', 'like_post__text')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentpost', 'user', 'comment')
    search_fields = ('user__username', 'commentpost__text', 'comment')
