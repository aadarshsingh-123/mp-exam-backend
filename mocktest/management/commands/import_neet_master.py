import json
import os
from django.core.management.base import BaseCommand
from mocktest.models import Question

class Command(BaseCommand):
    help = 'Import NEET questions from master JSON file'

    def handle(self, *args, **kwargs):
        json_file_path = r'E:\new Project\mp-exam-questions\neet-questions\all_neet_questions.json'
        
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return

        with open(json_file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        self.stdout.write(f"Loaded {len(questions)} questions from JSON. Preparing to save to DB...")
        
        # Clear existing NEET questions to avoid duplicates on multiple runs
        old_count = Question.objects.filter(exam_type='neet').count()
        Question.objects.filter(exam_type='neet').delete()
        self.stdout.write(f"Deleted {old_count} old NEET questions.")

        new_questions = []
        skip_count = 0

        for idx, q in enumerate(questions):
            try:
                opts = q.get('options', [])
                if len(opts) < 4:
                    skip_count += 1
                    continue
                
                # Basic parsing
                correct_opt = str(q.get('correct_opt', ''))
                
                # If correct_opt is just a single letter like 'A', map it to the actual full text
                if len(correct_opt) <= 2 and correct_opt.replace(')','').strip().upper() in ['A', 'B', 'C', 'D']:
                    letter = correct_opt.replace(')','').strip().upper()
                    correct_opt = opts[['A','B','C','D'].index(letter)]
                
                nq = Question(
                    category=q.get('category', 'NEET General')[:100],
                    text=q.get('text', ''),
                    opt1=opts[0],
                    opt2=opts[1],
                    opt3=opts[2],
                    opt4=opts[3] if len(opts) > 3 else opts[2],
                    correct_opt=correct_opt,
                    exam_name=q.get('exam_name', 'NEET')[:100],
                    year=q.get('year', '')[:20],
                    explanation=q.get('explanation', ''),
                    exam_type='neet'
                )
                new_questions.append(nq)
                
            except Exception as e:
                skip_count += 1
                self.stderr.write(f"Error parsing row {idx}: {str(e)}")
                
        if new_questions:
            # Chunking to avoid sqlite limits
            batch_size = 500
            for i in range(0, len(new_questions), batch_size):
                Question.objects.bulk_create(new_questions[i:i+batch_size])
                self.stdout.write(f"Inserted batch {i} to {i+batch_size}")
            
        self.stdout.write(self.style.SUCCESS(f'Successfully ingested {len(new_questions)} NEET questions! Skipped {skip_count}.'))
