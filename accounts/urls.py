from django.urls import path
from .views import LoginView, ProfileView, AdminAddStudentView, AdminStudentListView, AdminDeleteStudentView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Admin only
    path('admin/students/', AdminStudentListView.as_view(), name='admin-student-list'),
    path('admin/students/add/', AdminAddStudentView.as_view(), name='admin-add-student'),
    path('admin/students/<int:pk>/delete/', AdminDeleteStudentView.as_view(), name='admin-delete-student'),
]
