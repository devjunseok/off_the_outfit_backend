import requests
from bs4 import BeautifulSoup
from weather.models import Weather

# 네이버 날씨 크롤링
def forecast():

    cities = ['서울특별시',
            '인천광역시',
            '부산광역시',
            '대구광역시',
            '인천광역시',
            '광주광역시',
            '대전광역시',
            '울산광역시',
            '세종특별자치시',
            '경기도',
            '강원도',
            '충청북도',
            '충청남도',
            '전라북도',
            '전라남도',
            '경상북도',
            '경상남도',
            '제주특별자치도']

    for city in cities:

        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={city}날씨"


        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        res = requests.get(url, headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'lxml')
        week = soup.find("div", attrs={"class":"list_box _weekly_weather"})
        week = week.find_all("div", attrs={"class":"day_data"})
        for day in week:
            
            day_date = day.find("span", attrs={"class":"date"}).get_text() #날짜
            day_temperature_lowest = day.find("span", attrs={"class":"lowest"}).get_text() # 최저기온
            day_temperature_lowest = day_temperature_lowest.replace("최저기온", "").replace("°", "")
            day_temperature_highest = day.find("span", attrs={"class":"highest"}).get_text() # 최고기온
            day_temperature_highest = day_temperature_highest.replace("최고기온", "").replace("°", "")
            day_blind = day.find("span", attrs={"class":"blind"}).get_text() # 날씨 상태
            day_temperature = int(int(day_temperature_highest) + int(day_temperature_lowest)) / 2 # 평균 기온

            weather = Weather()
            weather.city = city
            weather.day_date = day_date
            weather.day_temperature_lowest = day_temperature_lowest
            weather.day_temperature_highest = day_temperature_highest
            weather.day_temperature = day_temperature
            weather.day_blind = day_blind
            weather.save()