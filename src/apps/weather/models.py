from django.db import models
from django.contrib.auth.models import User

class CitySearch(models.Model):
    city = models.CharField(max_length=100)
    session_key = models.CharField(max_length=40, default='') 
    count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("city", "session_key")

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    city = models.CharField(max_length=100)
    count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.city}"