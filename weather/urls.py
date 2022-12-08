from django.urls import path
from weather import views

urlpatterns = [

    path('', views.WeatherInfoView.as_view(), name='weather_view' ), # 네이버 날씨 크롤링 url

]
