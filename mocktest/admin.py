from django.contrib import admin
from .models import TestResult, Question

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_type', 'test_name', 'obtained_marks', 'total_marks', 'percentage', 'created_at']
    list_filter = ['test_type', 'test_name']
    search_fields = ['user__full_name', 'user__email']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam_type', 'category', 'exam_name', 'year', 'text']
    list_filter = ['exam_type', 'category', 'exam_name', 'year']
    search_fields = ['text', 'category', 'exam_name']
