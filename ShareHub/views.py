from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PostCreate, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import AuthorAccount
from django.shortcuts import get_object_or_404

class PostCreateView(APIView):
 
    def post(self, request):
        user_id = request.data.get('user')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AuthorAccount.objects.get(id=user_id)
        except AuthorAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(AuthorAccount, id=user_id)
            user_post = PostCreate.objects.filter(created_by=user)
        else:
            user_post = PostCreate.objects.all()

 
        serializer = PostSerializer(user_post, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(PostCreate, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        post = get_object_or_404(PostCreate, id=post_id)

        if post.created_by != request.user:
            return Response({"error": "You are not allowed to update this post"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(PostCreate, id=post_id)

        if post.created_by != request.user:
            return Response({"error": "You are not allowed to delete this post"},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(PostCreate, id=post_id)
        likes = Like.objects.filter(like_post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response({
            "like_count": likes.count(),
            "likes": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request, post_id):
        post = get_object_or_404(PostCreate, id=post_id)
        user = request.user

        existing_like = Like.objects.filter(like_post=post, user=user).first()

        if existing_like:
            existing_like.delete()
            like_count = Like.objects.filter(like_post=post).count()
            return Response(
                {'message': 'Like removed', 'like_count': like_count},
                status=status.HTTP_200_OK
            )

        Like.objects.create(like_post=post, user=user)
        like_count = Like.objects.filter(like_post=post).count()
        return Response(
            {'message': 'Like added', 'like_count': like_count},
            status=status.HTTP_201_CREATED
        )

class CommentsView(APIView):

    def post(self, request):
    
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Comment created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, comments_id=None):
        if comments_id:
            comment = get_object_or_404(Comment, id=comments_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)


        post_id = request.GET.get('post')
        if post_id:
            comments = Comment.objects.filter(commentpost_id=post_id)
        else:
            comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, comments_id):
        
        comment = get_object_or_404(Comment, id=comments_id, user=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comments_id):
    
        comment = get_object_or_404(Comment, id=comments_id, user=request.user)
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
