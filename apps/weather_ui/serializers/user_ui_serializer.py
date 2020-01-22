from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class UserUiRegisterSerializer(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField()
    username = serializers.CharField(
        label="",
        style={'input_type': 'text', 'placeholder': 'User Name'},
        validators=[UniqueValidator(queryset=UserModel.objects.all(), message="UserName Is already Exist")]

    )
    password = serializers.CharField(
        max_length=100,
        label="",
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    # def get_token(self, object):
    #     return Token.objects.get(user__username=object.username).key

    def create(self, validated_data):
        user, created = UserModel.objects.get_or_create(
            username=validated_data['username']
        )
        if not created:
            raise serializers.ValidationError("User with this username is exist", code='authorization')
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserUiLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label="",
        style={'input_type': 'text', 'placeholder': 'User Name'},

    )
    password = serializers.CharField(
        max_length=100,
        label="",
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = UserModel
        fields = ('username', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }
