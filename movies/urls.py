from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('rent/<int:movie_id>/', views.rent_movie, name='rent_movie'),
    path('return/<int:movie_id>/', views.return_movie, name='return_movie'),
    path('my-rented-movies/', views.my_rented_movies, name='my_rented_movies'),
    path('signup/', views.signup, name='signup'),
    
    path('logout/', views.logout_view, name='logout'),
]