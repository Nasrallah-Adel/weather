from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )

    def validate_username(self, username):
        return username.lower()

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
