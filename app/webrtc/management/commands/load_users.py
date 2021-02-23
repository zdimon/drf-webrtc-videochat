from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('creating superuser')
        u = User()
        u.username = 'admin'
        u.set_password('admin')
        u.is_active = True
        u.is_staff = True
        u.email = 'admin@gmail.com'
        u.is_superuser = True
        u.save()