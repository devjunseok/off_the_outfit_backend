from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.UserView.as_view(), name='user_view'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('follow/<int:user_id>/', views.FollowView.as_view(),name='follow_view'), # follow url
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'), # 회원 정보 상세 조회, 수정 url
    path('search/', views.UserSearchView.as_view(), name = 'articles_search_view'),  # 유저 검색 url
]