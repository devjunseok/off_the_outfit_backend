from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):

    def create_user(self, email, username, nickname, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, nickname, password=None):

        user = self.create_user(
            email,
            password=password,
            username=username,
            nickname=nickname,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
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

    username = models.CharField("아이디", max_length=20, unique=True, error_messages={'unique':"이미 존재하는 아이디입니다."})
    nickname = models.CharField("닉네임", max_length=16, unique=True, error_messages={'unique':"이미 존재하는 닉네임입니다."})
    email = models.EmailField("이메일", max_length=255,unique=True, error_messages={'unique':"이미 존재하는 이메일입니다."})
    profile_image = models.ImageField(default="imgs/default.png", blank=True, upload_to="profile_images/", null=True)
    address = models.CharField("주소", max_length=100)
    gender = models.CharField("성별", choices=GENDERS, max_length=1)
    status = models.CharField("상태", choices=USER_STATUS, max_length=10, default=USER_STATUS[0][0])
    roles = models.CharField("권한",  choices=ROLES, max_length=20, default=ROLES[0][0])
    date_of_birth = models.DateField("생년월일", null=True)
    height = models.CharField("키", max_length=20, blank=True)
    weight = models.CharField("몸무게", max_length=16, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    is_active = models.BooleanField("계정 활성화 여부", default=True)
    is_admin = models.BooleanField("관리자 권한", default=False)
    term_agree = models.BooleanField("약관동의", default=False)
    click_time = models.CharField("출석클릭시간", max_length=255, null=True)
    point = models.IntegerField("포인트", default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'nickname']


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
    

    