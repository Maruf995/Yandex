from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

from users.models import User


# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  
    author = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    created_date = models.DateField(auto_now_add=True, blank=True)

class Post(models.Model):
    text = models.TextField(max_length=500)
    created_date = models.DateField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    rating = models.ManyToManyField('Rating', related_name='posts', blank=True)
    comment = models.ManyToManyField(Comment,related_name='posts', blank=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return ratings.aggregate(models.Avg('mark_number'))['mark_number__avg']
        return None

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    auth = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    mark_number = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
