from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)
    runtime = models.IntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')  # good practice to add related_name

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']  # Optional: newest first

    def __str__(self):
        return f"{self.user.username} ➤ {self.movie.title}"
