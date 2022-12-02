
from django.core.management.base import BaseCommand, CommandError
from users.models import User
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '10일보다 오래된 objects를 지운다.'

    def handle(self, *args, **options):
        User.objects.filter(creating_date__lte=datetime.now()-timedelta(days=10)).delete()
        self.stdout.write('10일보다 오래된 유저 오브젝트를 제거합니다')