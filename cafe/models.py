from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
import datetime


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    is_owner = models.BooleanField()

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


class Cafe(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(upload_to='cafe_images', blank=True)
    pricepoint = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    address = models.TextField(default='1600 Amphitheatre Parkway, Mountain View, CA 94043')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Cafe, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cafes'

    def __str__(self):
        return self.name


class Review(models.Model):
    # linking reviews with Cafes
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # criteria to rate the cafe
    price = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    service = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    atmosphere = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    quality = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    waiting_time = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.CharField(max_length=500, blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    avg_rating = models.IntegerField(blank=True, default=0)

    class Meta:
        # joins cafe and user as primary keys
        unique_together = ('cafe', 'user')
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.user.user.username
