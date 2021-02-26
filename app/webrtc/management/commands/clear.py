from django.core.management.base import BaseCommand
from webrtc.models import UserProfile

class Command(BaseCommand):


    def handle(self, *args, **options):
        print('Clearing')
        UserProfile.objects.all().delete()