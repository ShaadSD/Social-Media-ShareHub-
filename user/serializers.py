from rest_framework import serializers
from .models import AuthorAccount, Follower
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = AuthorAccount
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data['is_active'] = False
        return AuthorAccount.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = AuthorAccount.objects.get(email=email)
        except AuthorAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data


class followerSerializers(serializers.ModelSerializer):
    main_user_username = serializers.CharField(source='main_user.username', read_only=True)
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    first_name = serializers.CharField(source='follower.first_name', read_only=True)
    last_name = serializers.CharField(source='follower.last_name', read_only=True)
    image = serializers.URLField(source='follower.image', read_only=True)
    main_user_image = serializers.URLField(source='main_user.image', read_only=True)
    class Meta:
        model = Follower
        fields = ['id', 'main_user', 'main_user_username', 'follower', 'follower_username','image','first_name','last_name','main_user_image']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class AuthorAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorAccount
        fields = ['id', 'username','first_name', 'last_name', 'image', 'bio','email', 'about', 'created_at']