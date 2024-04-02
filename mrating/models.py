from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    password = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return self.name
    
    
class Movie(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    rating = models.CharField(max_length=20)
    release_date = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
    
class MovieRating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()
    
    def __str__(self):
        return self.user_id
    