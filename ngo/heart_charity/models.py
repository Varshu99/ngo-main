from django.db import models

# Create your models here.
class Volunteer(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    subject=models.CharField(max_length=30)
    message=models.TextField()

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    message=models.TextField()

    def __str__(self):
        return self.name

class Cause(models.Model):
    name=models.CharField(max_length=30)
    img=models.ImageField()
    detail=models.CharField(max_length=500)
    raised=models.FloatField()
    goal=models.FloatField()

    def __str__(self):
        return self.name

class Donate(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    amount=models.FloatField()

    def __str__(self):
        return self.name
    
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# models.py
from django.db import models
class Event(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participant_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title