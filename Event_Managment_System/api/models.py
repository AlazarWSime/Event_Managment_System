#models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Needed for foreign keys
#from django.contrib.auth import get_user_model
from django.conf import settings


#User = get_user_model()

class User(AbstractUser):
    pass  # No extra fields for 



class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
       return f"{self.organization_name} ({self.user.username})"
    


class Attendee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name
    
class Event(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='EventCategory')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # ← ADD THIS LINE
    updated_at = models.DateTimeField(auto_now=True)  # ← ADD THIS LINE

    def __str__(self):
        return self.title
    
class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Create your models here.

class RSVP(models.Model):
    STATUS_CHOICES = [ 
        ("going", "Going"),
        ("maybe", "Maybe"),
        ("declined", "Declined"),
    ]

    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ("event", "attendee") # one RSVP per attendee per event

    def __str__(self):
        return f"{self.attendee.user.username} -> {self.event.title} ({self.status})"