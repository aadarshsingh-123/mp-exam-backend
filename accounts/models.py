from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    EXAM_TYPE_CHOICES = [
        ('other', 'Other (MP Exams - Default)'),
        ('neet', 'NEET'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    exam_type = models.CharField(
        max_length=10,
        choices=EXAM_TYPE_CHOICES,
        default='other',
        help_text='NEET students see NEET questions, Others see default MP exam questions'
    )
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.full_name or self.email
