from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'exam_type', 'profile_image']

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
            password=validated_data['password'],
            exam_type=validated_data.get('exam_type', 'other'),
            profile_image=validated_data.get('profile_image', None),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'username', 'is_staff', 'date_joined', 'exam_type', 'profile_image']


class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ['full_name', 'profile_image', 'password']

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class StudentListSerializer(serializers.ModelSerializer):
    tests_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'username', 'is_staff', 'date_joined', 'is_active', 'tests_count', 'exam_type', 'profile_image']

