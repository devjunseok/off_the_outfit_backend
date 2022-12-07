from django.db import models

# Create your models here.

class Weather(models.Model):
    city = models.CharField('지역명', max_length=10)
    day_date = models.CharField('날짜', max_length=10)
    day_temperature_highest = models.IntegerField('최고기온')
    day_temperature_lowest = models.IntegerField('최저기온')
    day_temperature = models.IntegerField('평균기온')
    day_blind = models.CharField('날씨상태', max_length=10)

    def __str__(self):
        return str(self.city)
    
    class Meta:
        db_table = "weather"