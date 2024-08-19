from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_coach = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Player(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    bio = models.TextField(blank=True)
    wing = models.CharField(max_length=50, blank=True)
    height = models.FloatField(null=True, blank=True)
    pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user_profile.user.username

class Coach(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    certification = models.CharField(max_length=100, blank=True)
    coaching_style = models.CharField(max_length=100, blank=True)
    pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user_profile.user.username

class UpcomingMatches(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    @property
    def is_played(self):
        current_date = timezone.now().date()
        if current_date > self.date:
            return True
        return False
    
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='teams_coached')
    players = models.ManyToManyField(Player, related_name='teams')
    training_time = models.DateTimeField(null=True, blank=True)
    training_venue = models.CharField(max_length=100, blank=True)
    # upcoming_matches = models.ForeignKey(UpcomingMatches, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.user_profile.user.username
