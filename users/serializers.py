from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'date_of_birth',
            'profile_photo'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'profile_image']



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
        )
    
    def create(self, validated_data):
        # Hash the password
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        
        token = RefreshToken.for_user(user)

        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }