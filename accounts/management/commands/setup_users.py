from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin and test students'

    def handle(self, *args, **options):
        # Create Admin
        if not User.objects.filter(email='admin@gmail.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='Aadarsh@123',
                full_name='Admin',
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS('✅ Admin created: admin@gmail.com / Aadarsh@123'))
        else:
            self.stdout.write(self.style.WARNING('Admin already exists'))

        # Create Test Students
        students = [
            {'email': 'rahul@test.com', 'full_name': 'Rahul Kumar', 'password': 'test1234'},
            {'email': 'priya@test.com', 'full_name': 'Priya Sharma', 'password': 'test1234'},
            {'email': 'amit@test.com', 'full_name': 'Amit Verma', 'password': 'test1234'},
        ]
        for s in students:
            if not User.objects.filter(email=s['email']).exists():
                username = s['email'].split('@')[0]
                User.objects.create_user(
                    username=username,
                    email=s['email'],
                    password=s['password'],
                    full_name=s['full_name'],
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Student created: {s['email']} / {s['password']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Student {s['email']} already exists"))
