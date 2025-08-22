#serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Event, Category, Organizer, Attendee, RSVP, EventCategory # import my event and category from models.py

User = get_user_model()


#-------------------
# User Registration
#-------------------

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

#----------------------
# Category Serializer
#---------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


#-------------------------
# Event Serializer
#-------------------------

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.organization_name') # read only
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only = True
    ) # write only

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'organizer', 'categories', 'start_date', 'end_date', 'created_at', 'updated_at']


#-------------------------
# orgainizer Serializer
#-------------------------

class OrganizerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # show username instead of just id

    class Meta:
        model = Organizer
        fields = ['id', 'user', 'organization_name']
        read_only_fields = ['user']
        extra_kwargs = {
            'organization_name': {'required': True}
        }


#-------------------------
# attendies Serializer
#-------------------------
    
class AttendeeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # show username instead of just id


    class Meta:
        model = Attendee
        fields = ['id', 'user']
        read_only_fields = ['user']
        extra_kwargs = {
            'company': {'required': False}
        }

#-----------------------------
# RSVP serializer
#-----------------------------

class RSVPSerializer(serializers.ModelSerializer):
    attendee_name = serializers.ReadOnlyField(source='attendee.user.username')
    event_title = serializers.ReadOnlyField(source='event.title')
    organizer_name = serializers.ReadOnlyField(source = 'event.organizer.organization_name')
   
    class Meta:
        model = RSVP
        fields = [
            'id', 'event', 'event_title', 'attendee', 'attendee_name', 'organizer_name', 'status', 'created_at'
        ]
        read_only_fields = ['attendee', 'created_at']

    def validate(self, data):
        if self.instance is None:
            event = data.get('event')
            attendee = data.get('attendee')

            if event and attendee and RSVP.objects.filter(event = event, attendee = attendee).exists():
                raise serializers.ValidationError("you have already RSVP'd to this event")
        return data