from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Follower,AuthorAccount
from rest_framework import status,generics
from .serializers import followerSerializers,PasswordChangeSerializer,AuthorAccountSerializer
from django.contrib.auth.hashers import check_password
from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework import status

class UserRegistrationApiView(APIView):
    permission_classes =[AllowAny]
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/api/user/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    permission_classes =[AllowAny]
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = AuthorAccount._default_manager.get(pk=uid)
    except(AuthorAccount.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response(serializer.errors, status=400)

class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
        

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data.get("new_password")
            confirm_password = serializer.validated_data.get("confirm_password")

            if new_password != confirm_password:
                return Response(
                    {"confirm_password": "Passwords do not match."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Password updated successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomResetPasswordRequestToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AuthorAccount.objects.get(email=email)
        except AuthorAccount.DoesNotExist:
            return Response({"error": "User with this email does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f'http://127.0.0.1:5500/reset_password_confirm.html?uid={uid}&token={token}'

        email_subject = "Reset Your Password"
        email_body = render_to_string('password_reset_email.html', {'reset_link': reset_link})
        email_message = EmailMultiAlternatives(email_subject, '', to=[email])
        email_message.attach_alternative(email_body, "text/html")
        email_message.send()

        return Response({"detail": "Check your email for password reset instructions."},
                        status=status.HTTP_200_OK)
    


class CustomResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        uidb64 = request.query_params.get('uid')
        token = request.query_params.get('token')

        if not uidb64 or not token:
            return Response({'error': 'UID and token are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = AuthorAccount.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, AuthorAccount.DoesNotExist):
            return Response({'error': 'Invalid user or token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'New password is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successful.'},
                        status=status.HTTP_200_OK)



class FollowerView(APIView):
    
    def post(self, request):
        main_user_id = request.data.get('main_user')
        follower_id = request.data.get('follower')

        if not main_user_id or not follower_id:
            return Response({"error": "main_user and follower are required."}, status=status.HTTP_400_BAD_REQUEST)

        if main_user_id == follower_id:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            main_user = AuthorAccount.objects.get(id=main_user_id)
            follower_user = AuthorAccount.objects.get(id=follower_id)
        except AuthorAccount.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if Follower.objects.filter(main_user=main_user, follower=follower_user).exists():
            return Response({"error": "Already following."}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follower.objects.create(main_user=main_user, follower=follower_user)
        serializer = followerSerializers(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        main_user = request.query_params.get('main_user')
        follower = request.query_params.get('follower')

        if main_user and follower:
            exists = Follower.objects.filter(main_user_id=main_user, follower_id=follower).exists()
            return Response({"is_followed": exists}, status=200)

        user_id = request.query_params.get('user_id')
        list_type = request.query_params.get('type')
        search_term = request.query_params.get('search', '').lower()

        if not user_id or not list_type:
            return Response(
                {"error": "user_id and type (followers/following) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = AuthorAccount.objects.get(id=user_id)
        except AuthorAccount.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if list_type == 'followers':
            data = Follower.objects.filter(main_user=user)
        elif list_type == 'following':
            data = Follower.objects.filter(follower=user)
        else:
            return Response({"error": "Invalid type"}, status=400)

        if search_term and list_type == 'followers':
            data = data.filter(follower__username__icontains=search_term)
        elif search_term and list_type == 'following':
            data = data.filter(main_user__username__icontains=search_term)

        serializer = followerSerializers(data, many=True)
        return Response(serializer.data, status=200)
  
    def delete(self, request):
        main_user_id = request.query_params.get('main_user')
        follower_id = request.query_params.get('follower')
        action = request.query_params.get('action', 'unfollow') 

        if not main_user_id or not follower_id:
            return Response({"error": "main_user and follower are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if action == 'remove_follower':
            try:
                follow_relation = Follower.objects.get(main_user_id=main_user_id, follower_id=follower_id)
            except Follower.DoesNotExist:
                return Response({"error": "Follower not found."}, status=status.HTTP_404_NOT_FOUND)

            follow_relation.delete()
            return Response({"message": "Follower removed successfully."}, status=status.HTTP_200_OK)

        elif action == 'unfollow':
            try:
                follow_relation = Follower.objects.get(main_user_id=follower_id, follower_id=main_user_id)
            except Follower.DoesNotExist:
                return Response({"error": "Follow relationship not found."}, status=status.HTTP_404_NOT_FOUND)

            follow_relation.delete()
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid action. Use 'unfollow' or 'remove_follower'."},
                            status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    """
    Returns profile details of any user by user_id.
    If user_id is not provided, return logged-in user's profile.
    """

    def get(self, request):
        user_id = request.query_params.get("user_id")
        if user_id is None:
            user = request.user
        else:
            try:
                user = AuthorAccount.objects.get(id=user_id)
            except AuthorAccount.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


        total_followers = Follower.objects.filter(main_user=user).count()
        total_following = Follower.objects.filter(follower=user).count()


        serializer = AuthorAccountSerializer(user)
        profile_data = serializer.data

        profile_data.update({
            "total_followers": total_followers,
            "total_following": total_following
        })

        return Response(profile_data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data

        user.username = data.get("username", user.username)
        user.first_name = data.get("firstName", user.first_name) 
        user.last_name = data.get("lastName", user.last_name)
        user.bio = data.get("bio", user.bio)
        user.about = data.get("about", user.about)
        image_url = data.get("image_url")
        if image_url:
            user.image = image_url

        user.save()
        serializer = AuthorAccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PeopleYouMayKnowView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        limit = int(request.GET.get("limit", 4))
        users = AuthorAccount.objects.exclude(id=user.id)

        followed_ids = Follower.objects.filter(follower=user).values_list("main_user_id", flat=True)
        users = users.exclude(id__in=followed_ids)
        users = users[:limit]
        serialized = []
        for u in users:
            data = AuthorAccountSerializer(u).data
            data["is_followed"] = Follower.objects.filter(follower=user, main_user=u).exists()
            serialized.append(data)

        return Response(serialized, status=status.HTTP_200_OK)