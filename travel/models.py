from django.db import models


class User(models.Model):
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    birth_date = models.DateTimeField()


class Location(models.Model):
    place = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    distance = models.PositiveIntegerField()


class Visit(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    visited_at = models.DateTimeField()
    mark = models.PositiveSmallIntegerField()

