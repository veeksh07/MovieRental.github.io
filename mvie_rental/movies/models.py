from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre)
    release_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    cast = models.TextField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)  # Add this line
    trailer_url = models.URLField(null=True, blank=True)
    is_rented = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class RentedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rented_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movie.title} rented by {self.user.username}"