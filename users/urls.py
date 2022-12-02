from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.UserView.as_view(), name='user_view'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('follow/<int:user_id>/', views.FollowView.as_view(),name='follow_view'), # follow url
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),# 비밀번호 변경
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'), # 회원 정보 상세 조회, 수정 url

]