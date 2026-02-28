import os
import json
import sys

# Setup Django path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from mocktest.models import Question

def load_data():
    questions_path = os.path.join(base_dir, 'all_questions.json')
    if not os.path.exists(questions_path):
        print(f"File not found: {questions_path}")
        return

    with open(questions_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} questions. Preparing to save to db...")
    
    # Check if empty so we don't duplicate on multiple runs
    if Question.objects.exists():
        print(f"Database already contains {Question.objects.count()} questions. Skipping import.")
        return

    batch_size = 500
    objs = []
    
    for item in data:
        q = Question(
            category=item.get('category', ''),
            text=item.get('text', ''),
            opt1=item.get('opt1', ''),
            opt2=item.get('opt2', ''),
            opt3=item.get('opt3', ''),
            opt4=item.get('opt4', ''),
            correct_opt=item.get('correct_opt', ''),
            exam_name=item.get('exam_name', ''),
            year=item.get('year', ''),
            explanation=item.get('explanation', '')
        )
        objs.append(q)

    Question.objects.bulk_create(objs, batch_size=batch_size)
    print(f"Successfully saved {len(objs)} questions to DB.")

if __name__ == '__main__':
    load_data()
