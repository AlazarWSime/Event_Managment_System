from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Needed for foreign keys
from django.contrib.auth import get_user_model
from django.conf import settings


#User = get_user_model()

class User(AbstractUser):
    pass  # No extra fields for 



class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
       return f"{self.organization} ({self.user.username})"
    


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
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='EventCategory')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Create your models here.
