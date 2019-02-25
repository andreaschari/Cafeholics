from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    #Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    is_owner = models.BooleanField()

    class Meta:
        verbose_name_plural = "User Profiles"
    def __str__(self):
        return self.user.username

class Review(models.Model):
    #linking reviews with Cafes
    cafe = models.ForeignKey(Cafes)
    user = models.ForeignKey(UserProfile)
    #criteria to rate the cafe
    price = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    service = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    atmosphere = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    quality = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    waiting_time = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.CharField(max_length = 500, blank = True)

    class Meta:
        verbose_name_plural = "Reviews"


class Cafe(models.Model):
    owner = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(upload_to='cafe_images', blank=True)
    pricepoint = IntegerField(max_length=50)

    class Meta:
        verbose_name_plural = "Cafes"

    def __str__(self):
        return self.name
