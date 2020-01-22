from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )

    def get_token(self, object):
        return Token.objects.get(user__username=object.username).key

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
        fields = ('id', 'username', 'password', 'token')
        read_only_fields = ('id', 'token')
        extra_kwargs = {
            'password': {'write_only': True}
        }
