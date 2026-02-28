from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        # Ensure unique username
        base = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1
        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=validated_data.get('full_name', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'username', 'is_staff', 'date_joined']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class StudentListSerializer(serializers.ModelSerializer):
    tests_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'username', 'is_staff', 'date_joined', 'is_active', 'tests_count']
