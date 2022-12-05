
# Generated by Django 4.1.3 on 2022-12-05 06:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': '이미 존재하는 아이디입니다.'}, max_length=20, unique=True, verbose_name='아이디')),
                ('nickname', models.CharField(error_messages={'unique': '이미 존재하는 닉네임입니다.'}, max_length=16, unique=True, verbose_name='닉네임')),
                ('email', models.EmailField(error_messages={'unique': '이미 존재하는 이메일입니다.'}, max_length=255, unique=True, verbose_name='이메일')),
                ('profile_image', models.ImageField(blank=True, default='imgs/default.png', null=True, upload_to='profile_images/')),
                ('address', models.CharField(max_length=100, verbose_name='주소')),
                ('gender', models.CharField(choices=[('M', '남성(Man)'), ('W', '여성(Woman)')], max_length=1, verbose_name='성별')),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('STOP', 'STOP'), ('PAUSE', 'PAUSE'), ('BAN', 'BAN')], default='ACTIVE', max_length=10, verbose_name='상태')),
                ('roles', models.CharField(choices=[('ROLE_NORMAL', 'NORMAL'), ('ROLE_MANAGER', 'MANAGER'), ('ROLE_SUPER', 'SUPER')], default='ROLE_NORMAL', max_length=20, verbose_name='권한')),
                ('date_of_birth', models.DateField(null=True, verbose_name='생년월일')),
                ('height', models.CharField(max_length=20, verbose_name='키')),
                ('weight', models.CharField(max_length=16, verbose_name='몸무게')),
                ('is_active', models.BooleanField(default=True, verbose_name='계정 활성화 여부')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자 권한')),
                ('term_agree', models.BooleanField(default=False, verbose_name='약관동의')),
                ('click_time', models.CharField(max_length=255, null=True, verbose_name='출석클릭시간')),
                ('point', models.PositiveIntegerField(default=0, verbose_name='포인트')),
                ('followings', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
