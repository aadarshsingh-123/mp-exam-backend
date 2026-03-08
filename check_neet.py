import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from mocktest.models import Question
total = Question.objects.filter(exam_type='neet').count()
print(f'Total NEET questions: {total}')
cats = Question.objects.filter(exam_type='neet').values_list('category', flat=True).distinct()
print(f'Total categories: {len(cats)}')
for c in sorted(cats):
    cnt = Question.objects.filter(exam_type='neet', category=c).count()
    print(f'  {c}: {cnt}')
