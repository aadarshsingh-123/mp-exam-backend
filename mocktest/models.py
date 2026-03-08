from django.db import models
from django.conf import settings


class TestResult(models.Model):
    TEST_TYPE_CHOICES = [
        ('subject', 'Subject-wise'),
        ('full', 'Full Length'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES)
    test_name = models.CharField(max_length=200)
    total_questions = models.IntegerField()
    correct = models.IntegerField()
    wrong = models.IntegerField()
    skipped = models.IntegerField()
    total_marks = models.FloatField()
    obtained_marks = models.FloatField()
    percentage = models.FloatField()
    time_taken_seconds = models.IntegerField(default=0)  # how many seconds the user took
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.test_name} - {self.obtained_marks}/{self.total_marks}"

class Question(models.Model):
    EXAM_TYPE_CHOICES = [
        ('other', 'Other (MP Exams - Default)'),
        ('neet', 'NEET'),
    ]

    category = models.CharField(max_length=100)
    text = models.TextField()
    opt1 = models.TextField()
    opt2 = models.TextField()
    opt3 = models.TextField()
    opt4 = models.TextField()
    correct_opt = models.TextField()
    exam_name = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    exam_type = models.CharField(
        max_length=10,
        choices=EXAM_TYPE_CHOICES,
        default='other',
        help_text='NEET questions are shown only to NEET students'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.exam_type.upper()}][{self.category}] {self.text[:50]}"
