from django.core.management.base import BaseCommand, CommandError
from users.models import User
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '365일보다 오래된 objects를 지운다.'

    def handle(self, *args, **options):
        User.objects.filter(last_login__lte=datetime.now()-timedelta(days=365)).delete()
        self.stdout.write('365일보다 오래된 유저 오브젝트를 제거합니다')