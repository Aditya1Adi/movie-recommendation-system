from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Movies(models.Model):
    imdb_id = models.CharField(max_length=48, null=False)
    # Movie genres
    genres = models.CharField(max_length=200, null=True)
    # Original language
    original_language = models.CharField(max_length=20, null=True)
    # Original movie title
    original_title = models.CharField(max_length=500, null=False)
    # Movie release date
    release_date = models.IntegerField(default=1970)
    # Movie overview
    overview = models.TextField(max_length=2000, null=True)
    # Average voting for the movie
    vote_average = models.FloatField(default=0)
    # Total votes for ths movie
    vote_count = models.IntegerField(default=0)
    # The movie's poster path
    poster_path = models.CharField(max_length=64, null=True)
    # If you have watched this movie
    watched = models.BooleanField(default=False, null=True)
    # If this movie will be recommended
    recommended = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.original_title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for the user profile (e.g., profile picture, bio, etc.)
    # Example:
    # profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    # bio = models.TextField(blank=True)
    def __str__(self):
        return f'{self.user.username} UserProfile'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Watch List: {self.movie.original_title} ({self.rating})"

class BucketList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Bucket List: {self.movie.title}"

    def remove_from_bucket_list(self):
        self.delete()

