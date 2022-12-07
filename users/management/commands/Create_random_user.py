from django.core.management.base import BaseCommand
from users.models import User
from django_seed import Seed
import random

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help= "How many do you want Create User"
        )
    
    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        cities = ['서울특별시',
            '인천광역시',
            '부산광역시',
            '대구광역시',
            '인천광역시',
            '광주광역시',
            '대전광역시',
            '울산광역시',
            '세종특별자치시',
            '경기도',
            '강원도',
            '충청북도',
            '충청남도',
            '전라북도',
            '전라남도',
            '경상북도',
            '경상남도',
            '제주특별자치도']
        r_city = random.choice(cities)
        r_height = random.choice(list(range(140,210)))
        r_weight = random.choice(list(range(35,150)))
        seeder.add_entity(User, number, {
            "address":r_city,
            "gender": random.choice(['M','W']),
            "height":r_height,
            "weight":r_weight,
            "term_agree":True,
            "click_time":None,
            "is_admin":"0",
            "password":"password"
        })
        seeder.execute()
        
        self.stdout.write(self.style.SUCCESS(f"{number} 명의 더미 유저 생성 완료!"))