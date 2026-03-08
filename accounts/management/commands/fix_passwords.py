from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import is_password_usable, identify_hasher

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix passwords for users that may have plain text passwords (re-hash them)'

    def handle(self, *args, **options):
        users = User.objects.all()
        fixed = 0

        for user in users:
            # Check if the password looks like a valid hashed password
            try:
                identify_hasher(user.password)
                self.stdout.write(f"✅ {user.email} - password is already hashed correctly")
            except ValueError:
                # Password is NOT hashed (likely plain text from ModelAdmin)
                plain_password = user.password
                user.set_password(plain_password)
                user.save()
                fixed += 1
                self.stdout.write(self.style.WARNING(
                    f"🔧 {user.email} - password was plain text, now hashed"
                ))

        if fixed == 0:
            self.stdout.write(self.style.SUCCESS('\n✅ All passwords were already hashed correctly!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Fixed {fixed} user(s) with plain text passwords'))
