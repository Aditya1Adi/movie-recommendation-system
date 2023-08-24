from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('movie_search/',views.movie_search,name='movie_search'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('movie_detail/<str:imdb_id>/',views.movie_detail,name='movie_detail'),
    path('bucket_list/',views.bucket_list,name='bucket_list'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('movie_recommendations/<str:imdb_id>/',views.movie_recommendations,name='movie_recommendations'),
    path('add_to_bucket_list/<str:imdb_id>/', views.add_to_bucket_list, name='add_to_bucket_list'),
    path('bucket_list/', views.bucket_list, name='bucket_list'),
    path('remove_from_bucket_list/<str:imdb_id>/', views.remove_from_bucket_list, name='remove_from_bucket_list'),
    path('watch_list/', views.watch_list, name='watch_list'),
    path('add_to_watch_list/<str:imdb_id>/',views.add_to_watch_list,name='add_to_watch_list'),
]

