from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.UserView.as_view(), name='user_view'),                                          # 회원가입, 회원정보 수정, 회원정보 삭제 url
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),       # 로그인 url
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),                  # 리프레쉬 토근 url
    
    path('kakao/callback/', views.KakaoLoginView.as_view(), name='kakao_callback'),# 카카오 소셜로그인 url
    # path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),# 카카오 소셜로그인 url
    
    # path('social/', views.SocialLoginView.as_view(), name='social_login_view'),
    path('follow/<int:user_id>/', views.FollowView.as_view(),name='follow_view'),                  # follow url
    path('passwordchange/', views.PasswordChangeView.as_view(), name='passwordchange_view'),       # 비밀번호 변경 url
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),                      # 회원 정보 상세 조회, 수정 url
    path('<int:user_id>/followings/', views.GetFollowingsView.as_view(), name='followings_view'),  # 팔로잉 유저 조회
    path('<int:user_id>/followers/', views.GetFollowersView.as_view(), name='followers_view'),     # 팔로워 유저 조회
    path('search/', views.UserSearchView.as_view(), name = 'users_search_view'),                   # 유저 검색 url
    path('point/<int:user_id>/', views.GetPointView.as_view(), name='get_point_view'),             # 버튼 클릭 포인트 획득 url
    ##이메일 패스워드 리셋
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]