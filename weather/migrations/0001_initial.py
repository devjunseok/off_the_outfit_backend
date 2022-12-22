

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[

                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=50, verbose_name="지역명")),
                ("day_date", models.CharField(max_length=50, verbose_name="날짜")),
                ("day_temperature_highest", models.IntegerField(verbose_name="최고기온")),
                ("day_temperature_lowest", models.IntegerField(verbose_name="최저기온")),
                ("day_temperature", models.IntegerField(verbose_name="평균기온")),
                ("day_blind", models.CharField(max_length=50, verbose_name="날씨상태")),
            ],
            options={
                'db_table': 'weather',
            },
        ),
    ]
