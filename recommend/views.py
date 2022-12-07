import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from articles.models import Movie
from recommend.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

trends = pd.read_csv('trend.csv')
netflix = pd.read_csv('netflix.csv')

movie_ratings = pd.merge(trends, netflix, on='movie_id')

user_title = movie_ratings.pivot_table('rating_x', index='movie_id', columns='user_id')
user_title = user_title.fillna(0)

item_based_collab = cosine_similarity(user_title, user_title)
item_based_collab = pd.DataFrame(item_based_collab, index=user_title.index, columns=user_title.index)

class TasteView(APIView): # 영화 추천 View
    
    def get(self, request, movie_id):
        movie_id_list = item_based_collab[movie_id].sort_values(ascending=False)[1:21]
        movie_id_list = [x for x in movie_id_list.keys()]
        movies = Movie.objects.filter(movie_id__in=movie_id_list)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class MovieRefresh(APIView): # 영화 새로고침 View
    
    def get(self, request):
        movie = Movie.objects.filter(rating__gt=0).order_by('?')
        movie = list(movie)[0:10]
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
## 