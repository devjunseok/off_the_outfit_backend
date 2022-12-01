from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def validate(self, data):
        return data    
    
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password) # 패스워드 해싱
        user.save()
        return user
    
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password) # 패스워드 해싱
        user.save()
        return user 