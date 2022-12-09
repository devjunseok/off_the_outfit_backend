from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.UserView.as_view(), name='user_view'), # 회원가입, 회원정보 수정, 회원정보 삭제 url
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # 로그인 url
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 리프레쉬 토근 url
    path('follow/<int:user_id>/', views.FollowView.as_view(),name='follow_view'), # follow url
    path('passwordchange/', views.PasswordChangeView.as_view(), name='passwordchange_view'), # 비밀번호 변경 url
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'), # 회원 정보 상세 조회, 수정 url
    path('search/', views.UserSearchView.as_view(), name = 'articles_search_view'),  # 유저 검색 url
    path('point/<int:user_id>/', views.GetPointView.as_view(), name='get_point_view'), # 버튼 클릭 포인트 획득 url
]