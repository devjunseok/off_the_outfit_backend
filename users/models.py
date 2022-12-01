from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

USER_STATUS = (
    ('ACTIVE',  'ACTIVE'), # 정상
    ('STOP', 'STOP'), # 정지(탈퇴)
    ('PAUSE', 'PAUSE'), # 계정 휴면
    ('BAN', 'BAN'), # 계정 정지
)


ROLES = (
    ('ROLE_NORMAL', 'NORMAL'), # 일반 사용자
    ('ROLE_MANAGER', 'MANAGER'), # 일반 관리자
    ('ROLE_SUPER', 'SUPER'), # 슈퍼 관리자
    )


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):  #createsuperuser 사용시 해당 함수 실행
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )

    username = models.CharField("아이디", max_length=20, unique=True)
    nickname = models.CharField("닉네임", max_length=16, unique=True)
    email = models.EmailField("이메일", max_length=255,unique=True)
    profile_image = models.ImageField(default="imgs/default.png", blank=True, upload_to="profile_images/", null=True)
    address = models.CharField("주소", max_length=100)
    gender = models.CharField("성별", choices=GENDERS, max_length=1)
    status = models.CharField("상태", choices=USER_STATUS, max_length=10, default=USER_STATUS[0][0])
    date_of_birth = models.DateField("생년월일")
    point = models.PositiveIntegerField("포인트", default=0)
    height = models.CharField("키", max_length=20)
    weight = models.CharField("몸무게", max_length=16)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    is_active = models.BooleanField("계정 활성화 여부", default=True)
    is_admin = models.BooleanField("관리자 권한", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
    
    
    def get_id(self):
        return self.id
    
    def __str__(self):
        return f"[유저] pk: {self.id} / 아이디: {self.username} / 닉네임: {self.nickname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

# 권한 테이블 모델
class Auth(models.Model):
    user = models.ForeignKey(User, related_name='auths', on_delete=models.CASCADE)
    role = models.CharField("권한설정", choices=ROLES, max_length=30, default=ROLES[0][0])