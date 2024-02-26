from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=1000, null=True, default=None, blank=True)
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return f"{self.user}'s post | Post ID: {self.id}"


#Using followers and follows makes it easier to query if databease is bigger.
#To check follows it does not require iterating over every user. Everything is stored in 2 structured collumns.
#But it makes data management harder. It requires changing data in to 2 places and making sure there is no errors. 
#Help text: https://www.geeksforgeeks.org/help_text-django-built-in-field-validation/
class Follow_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow_data")
    followers = models.ManyToManyField(User, related_name="followers", blank=True, help_text="Better do not change in admin panel. Change required in 2 places: user follows, other user's followers")
    follows = models.ManyToManyField(User, related_name="follows", blank=True, help_text="Better do not change in admin panel. Change required in 2 places: user follows, other user's followers")

    def __str__(self):
        return f"{self.user}'s follow data"