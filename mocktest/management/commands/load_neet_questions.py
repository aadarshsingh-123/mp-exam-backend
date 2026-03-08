import importlib
from django.core.management.base import BaseCommand
from mocktest.models import Question


class Command(BaseCommand):
    help = 'Load NEET Biology questions into the database'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing NEET questions before loading')

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count, _ = Question.objects.filter(exam_type='neet').delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing NEET questions.'))

        # Import all data modules
        data_modules = [
            'mocktest.management.commands.neet_bio_data1',
            'mocktest.management.commands.neet_bio_data2',
            'mocktest.management.commands.neet_bio_data3',
            'mocktest.management.commands.neet_bio_data4',
        ]

        total_created = 0
        total_skipped = 0

        for module_name in data_modules:
            try:
                mod = importlib.import_module(module_name)
                bio_data = mod.bio_data
                self.stdout.write(f'Loading from {module_name}...')
            except ImportError as e:
                self.stdout.write(self.style.WARNING(f'Skipping {module_name}: {e}'))
                continue

            for category, questions in bio_data.items():
                for q_tuple in questions:
                    text, options, correct_letter, exam_info, explanation = q_tuple

                    # Map correct letter to the full option text
                    letter_map = {'A': options[0], 'B': options[1], 'C': options[2], 'D': options[3]}
                    correct_opt = letter_map.get(correct_letter, options[0])

                    # Check for duplicates
                    if Question.objects.filter(text=text, exam_type='neet').exists():
                        total_skipped += 1
                        continue

                    Question.objects.create(
                        category=category,
                        text=text,
                        opt1=options[0],
                        opt2=options[1],
                        opt3=options[2],
                        opt4=options[3],
                        correct_opt=correct_opt,
                        exam_name=exam_info,
                        explanation=explanation,
                        exam_type='neet',
                    )
                    total_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {total_created} | Skipped (duplicates): {total_skipped} | Total NEET questions now: {Question.objects.filter(exam_type="neet").count()}'
        ))
