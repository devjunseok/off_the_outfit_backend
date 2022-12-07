from django.core.management.base import BaseCommand
from users.models import User
from products.models import Closet, Product
from django_seed import Seed
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help= "How many do you want Create User"
        )
    
    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        
        users = User.objects.all()
        products = Product.objects.all()
        
        seeder.add_entity(Closet, number, {
            "user": lambda x: random.choice(users),
            "product": lambda x: random.choice(products),
            "name_tag_id": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        })
        seeder.execute()
        
        self.stdout.write(self.style.SUCCESS(f"{number} 옷장 더미 생성 완료!"))