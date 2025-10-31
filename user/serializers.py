from rest_framework import serializers
from .models import AuthorAcount, Follower, Following

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = AuthorAcount
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
        return AuthorAcount.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.Serializer):
      username = serializers.CharField()
      password = serializers.CharField(write_only=True)


class followerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Follower
        fields = ['id','main_user','follower','follower_username']

class followingrSerializers(serializers.ModelSerializer):
    class Meta:
        model=Following
        fields = ['id','main_user','following','following_username']