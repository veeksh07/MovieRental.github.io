from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from datetime import datetime
from .models import Movie, RentedMovie, Genre
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(title__icontains=search_query)
    
    # Filter by genre
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        movies = movies.filter(genre__name=genre_filter)
    
    # Filter by release year
    year_filter = request.GET.get('year', '')
    if year_filter:
        movies = movies.filter(release_year=year_filter)
    
    # Filter by rating
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        movies = movies.filter(rating__gte=float(rating_filter))
    
    # Sort functionality
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'rating':
        movies = movies.order_by('-rating')
    elif sort_by == 'year':
        movies = movies.order_by('-release_year')
    elif sort_by == 'title':
        movies = movies.order_by('title')
    
    # Get top rated movies
    top_rated = Movie.objects.filter(rating__gte=8.0).order_by('-rating')[:5]
    
    # Get latest movies (last 5 years)
    current_year = datetime.now().year
    latest = Movie.objects.filter(release_year__gte=current_year-5).order_by('-release_year')[:5]
    
    # Mark rented movies
    if request.user.is_authenticated:
        user_rented = RentedMovie.objects.filter(user=request.user).values_list('movie_id', flat=True)
        for movie in movies:
            if movie.id in user_rented:
                movie.user_rented = True
    
    # Get unique years for filtering
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    context = {
        'movies': movies,
        'genres': genres,
        'years': years,
        'top_rated': top_rated,
        'latest': latest,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'year_filter': year_filter,
        'rating_filter': rating_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'movies/home.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_rented = False
    
    if request.user.is_authenticated:
        user_rented = RentedMovie.objects.filter(user=request.user, movie=movie).exists()
    
    context = {
        'movie': movie,
        'user_rented': user_rented,
    }
    
    return render(request, 'movies/movie_detail.html', context)

@login_required
def rent_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Check if movie is already rented
    if movie.is_rented:
        return redirect('movie_detail', movie_id=movie_id)
    
    # Create rental record
    RentedMovie.objects.create(user=request.user, movie=movie)
    
    # Mark movie as rented
    movie.is_rented = True
    movie.save()
    
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def return_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    rental = get_object_or_404(RentedMovie, user=request.user, movie=movie)
    
    # Delete rental record
    rental.delete()
    
    # Mark movie as available
    movie.is_rented = False
    movie.save()
    
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def my_rented_movies(request):
    rentals = RentedMovie.objects.filter(user=request.user)
    
    context = {
        'rentals': rentals,
    }
    
    return render(request, 'movies/my_rented_movies.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})