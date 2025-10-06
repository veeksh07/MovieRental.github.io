import json
import os
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads movies from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'movies.json')
        
        with open(file_path, 'r') as file:
            movies_data = json.load(file)
        
        for movie_data in movies_data:
            # Create or get genres
            genres = []
            for genre_name in movie_data['genres']:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                genres.append(genre)
            
            # Create movie
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'release_year': movie_data['release_year'],
                    'rating': movie_data['rating'],
                    'description': movie_data['description'],
                    'cast': movie_data['cast'],
                    'trailer_url': movie_data.get('trailer_url', ''),
                    'poster_url': movie_data.get('poster', ''),  # Store external poster URL
                }
            )
            
            # Add genres to movie
            for genre in genres:
                movie.genre.add(genre)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded movies'))