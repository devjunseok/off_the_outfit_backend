import re

from users.models import User
from products.serializers import NameTagViewSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


# 회원가입 serializer
class UserSerializer(serializers.ModelSerializer): 
    password2= serializers.CharField(error_messages={'required':'비밀번호를 입력해주세요.', 'blank':'비밀번호를 입력해주세요.', 'write_only':True})
    class Meta:
        model = User
        fields = ('username', 'term_agree', 'email', 'nickname', 'nickname', 'address', 'gender', 'height', 'weight', 'date_of_birth', 'password', 'password2', 'profile_image',)
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'required': '아이디를 입력해주세요.',
                    'blank':'아이디를 입력해주세요.',
                    },
                    'required': True # default : True
                    },
            'email': {
                'error_messages': {
                    'required': '이메일을 입력해주세요.',
                    'blank':'이메일을 입력해주세요.',
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    'required': True # default : True
                    },
            'nickname': {
                'error_messages': {
                    'required': '닉네임을 입력해주세요.',
                    'blank':'닉네임을 입력해주세요.',
                    },
                    'required': True # default : True
                    },
            'address': {
                'error_messages': {
                    'required': '주소를 입력해주세요.',
                    'blank':'주소를 입력해주세요.',
                    },
                    'required': True # default : True
                    },
            'gender': {
                'error_messages': {
                    'required': '성별을 선택해주세요.',
                    'blank':'성별을 선택해주세요.',
                    'invalid': '알맞은 성별을 선택해주세요!'
                    },
                    'required': True # default : True
                    },
            'height': {
                'error_messages': {
                    'required': '키를 입력해주세요.',
                    'blank':'키를 입력해주세요.',
                    'invalid': '숫자만 입력 가능합니다.'
                    },
                    'required': True # default : True
                    },
            'weight': {
                'error_messages': {
                    'required': '몸무게를 입력해주세요',
                    'blank':'몸무게를 입력해주세요.',
                    'invalid': '숫자만 입력 가능합니다'
                    },
                    'required': True # default : True
                    },
            'date_of_birth': {
                'error_messages': {
                    'required': '생년월일을 입력해주세요.',
                    'blank':'생년월일을 입력해주세요.',
                    'invalid': 'YYYY-MM-DD 형식으로 생년월일을 입력해주세요!'
                    },
                    'required': True # default : True
                    },
            'password': {
                'error_messages': {
                    'required': '비밀번호를 입력해주세요.',
                    'blank':'비밀번호를 입력해주세요.',
                    },
                    'required': True,
                    'write_only': True# default : True
                    },
            'term_agree': {
                'error_messages': {
                    'required': '개인정보 약관 동의를 해주세요!',
                    'blank':'개인정보 약관 동의를 해주세요!',
                    'invalid': '알맞은 형식으로 해주세요!'
                    },
                    'required': True # default : True
                    },
            }
        
    def validate(self, data):
        PASSWORD_VALIDATION = r"^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}"
        PASSWORD_PATTERN = r"(.)\1+\1"
        USERNAME_VALIDATION = r"^(?=.*[$@$!%*?&]){1,2}"
        NICKNAME_VALIDATION = r"^(?=.*[$@$!%*?&])"
        ADDRESS_VALIDATION = r"^(?=.*[$@$!%*?&])"
        
        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')
        password2 = data.get('password2')
        address = data.get('address')
        term_agree = data.get('term_agree')
        
        
        if re.search(NICKNAME_VALIDATION, str(nickname)): # 닉네임 유효성 검사
            raise serializers.ValidationError(detail={"nickname":"닉네임에는 특수문자가 포함될 수 없습니다!"})
        
        if re.search(USERNAME_VALIDATION, str(username)): # 아이디 유효성 검사
            raise serializers.ValidationError(detail={"username":"아이디에는 특수문자가 포함될 수 없습니다!"})
        
        if re.search(ADDRESS_VALIDATION, str(address)): # 주소 유효성 검사
            raise serializers.ValidationError(detail={"address":"주소에는 특수문자가 포함될 수 없습니다!"})
    
        
        if password: # 비밀번호 유효성 검사
            if password != password2:
                raise serializers.ValidationError(detail={"password":"비밀번호 확인이 일치하지 않습니다!"})
            
            if not re.search(PASSWORD_VALIDATION, str(password)):
                raise serializers.ValidationError(detail={"password":"비밀번호는 8자 이상 16자이하의 영문, 숫자, 특수문자 조합이어야 합니다! "})
            
            if re.search(PASSWORD_PATTERN, str(password)):
                raise serializers.ValidationError(detail={"password":"너무 일상적인 숫자or단어 입니다!"})
        
        if term_agree == False:
            raise serializers.ValidationError(detail={"term_agree":"개인정보 약관 동의를 확인해주세요!"})
            

        return data    
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        nickname = validated_data['nickname']
        address = validated_data['address']
        height = validated_data['height']
        weight = validated_data['weight']
        date_of_birth = validated_data['date_of_birth']
        gender = validated_data['gender']
        term_agree = validated_data['term_agree']

        user = User(
            username=username,
            email=email,
            nickname=nickname,
            address=address,
            height=height,
            weight=weight,
            date_of_birth=date_of_birth,
            gender=gender,
            term_agree=term_agree
        )
        user.set_password(validated_data['password']) # 패스워드 해싱
        user.save()
        return user
    
    def update(self, instance, validated_data): # 회원정보 수정
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        
        return instance
    



# TokenObtainPairSerializer 커스텀 serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):   
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    default_error_messages = {"no_active_account": _("아이디 or 비밀번호를 확인해주세요. ")}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # self.user.last_login = timezone.now()
        # self.user.save()
        # Add extra responses here
        data['id'] = self.user.id
        data['username'] = self.user.username
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # if token['username'] == user.username:
        #     login_point = User.objects.get(User.point)
        #     login_point =+10
        #     return token,login_point
        token['username'] = user.username

        return token

# 회원정보 조회 serializer
class UserProfileSerializer(serializers.ModelSerializer): 
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    feeds_count = serializers.SerializerMethodField()
    closet_set_count = serializers.SerializerMethodField()
    nametag_set = serializers.SerializerMethodField()
    
    def get_nametag_set(self, instance):
        nametag = instance.nametag_set.all()
        return NameTagViewSerializer(nametag, many=True).data
    
    def get_followings_count(self, obj):
        return obj.followings.count()
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_feeds_count(self, obj):
        return obj.feeds.count()
    
    def get_closet_set_count(self,obj):
        return obj.closet_set.count()
    
    class Meta:
        model = User
        fields = ('pk', 'username', 'nametag_set', 'closet_set_count', 'feeds_count', 'nickname', 'email', 'address', 'gender', 'height', 'weight', 'date_of_birth', 'profile_image', 'point', 'followings_count', 'followers_count', 'followings', 'followers')

# 패스워드 변경 serializer
class PasswordChangeSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(error_messages={'required':'비밀번호를 입력해주세요.', 'blank':'비밀번호를 입력해주세요.', 'write_only':True})
    
    class Meta:
        model = User
        fields=("password","password2",)
    
    def validate(self, data):
        PASSWORD_VALIDATION = r"^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}"
        PASSWORD_PATTERN = r"(.)\1+\1"
        
        current_password = self.context.get("request").user.password
        password = data.get('password')
        password2 = data.get('password2')
        
        #현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password":"현재 비밀번호와 동일합니다!."})
        
        #비밀번호 일치
        if password != password2:
            raise serializers.ValidationError(detail={"password":"비밀번호 확인이 일치하지 않습니다!"})
        
        #비밀번호 유효성 검사
        if not re.search(PASSWORD_VALIDATION, str(password)):
            raise serializers.ValidationError(detail={"password":"비밀번호는 8자 이상 16자이하의 영문, 숫자, 특수문자 조합이어야 합니다! "})
        
        #비밀번호 문자열 동일여부 검사
        if re.search(PASSWORD_PATTERN, str(password)):
            raise serializers.ValidationError(detail={"password":"너무 일상적인 숫자or단어 입니다!"})

        return data
    
    
    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance