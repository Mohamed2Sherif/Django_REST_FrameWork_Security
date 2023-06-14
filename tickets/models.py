from django.db import models

# Create your models here.

#guest -- Movie -- reversation
class Movie(models.Model):
    hall = models.CharField(max_length=10,)
    movie = models.CharField(max_length=10)
    date = models.DateField()


class Guest(models.Model):
    Name = models.CharField(max_length=255, unique=True)
    mobile = models.CharField(max_length=23,)
class Reservation(models.Model):
    guest = models.ForeignKey(Guest,related_name = "reservation", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name = "reservation", on_delete=models.CASCADE)
