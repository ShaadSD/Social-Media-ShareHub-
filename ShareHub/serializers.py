from rest_framework import serializers
from .models import PostCreate, Like, Comment
from user.models import AuthorAccount
from user.serializers import AuthorAccountSerializer
class PostSerializer(serializers.ModelSerializer):
    created_by = AuthorAccountSerializer(read_only=True) 
    class Meta:
        model = PostCreate
        fields = ['id', 'text', 'image', 'video', 'created_by', 'created_at']
        extra_kwargs = {
            'text': {'required': False, 'allow_blank': True, 'allow_null': True}
        }
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'like_post', 'user']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.CharField(source='user.image', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'commentpost', 'user', 'comment', 'username', 'image']
        read_only_fields = ['user']