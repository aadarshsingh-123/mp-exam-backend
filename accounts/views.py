from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Count
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, StudentListSerializer

User = get_user_model()


class LoginView(APIView):
    """Login for all users (students and admin)."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })


class ProfileView(APIView):
    """Get current user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ===== ADMIN ONLY ENDPOINTS =====

class AdminAddStudentView(APIView):
    """Admin adds a new student."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class AdminStudentListView(APIView):
    """Admin sees all students."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = User.objects.filter(is_staff=False).annotate(
            tests_count=Count('test_results')
        ).order_by('-date_joined')
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)


class AdminDeleteStudentView(APIView):
    """Admin deletes a student."""
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            student = User.objects.get(pk=pk, is_staff=False)
            student.delete()
            return Response({'message': 'Student deleted'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
