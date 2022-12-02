from django.urls import path
from communities import views

urlpatterns = [
    path('', views.ArticlesFeedView.as_view(), name ='feed_list' ), # 게시글 전체보기
]
