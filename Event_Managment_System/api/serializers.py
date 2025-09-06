#serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Event, Category, Organizer, Attendee, RSVP, EventCategory # import my event and category from models.py
from drf_spectacular.utils import extend_schema_field, OpenApiTypes


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
    events = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'events']

    def get_events(self, obj):
        events = Event.objects.filter(categories=obj)
        return [
            {
                "id": event.id,
                "title": event.title,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "location": event.location,
                "organizer": event.organizer.organization_name
            }
            for event in events
        ]


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
    def validate(self, data):
        try:
            user = self.context['request'].user
            if Attendee.objects.filter(user=user).exists():
                raise serializers.ValidationError({
                    "error": "User is already registered as an attendee",
                    "code": "duplicate_attendee"
                })
            return data
        except Exception as e:
            raise serializers.ValidationError({
                "error": "Validation failed",
                "code": "validation_error",
                "details": str(e)
            })

#-----------------------------
# RSVP serializer
#-----------------------------

class RSVPSerializer(serializers.ModelSerializer):
    attendee_name = serializers.ReadOnlyField(source='attendee.user.username')
    event_title = serializers.ReadOnlyField(source='event.title')
    organizer_name = serializers.ReadOnlyField(source='event.organizer.organization_name')
    
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    status = serializers.ChoiceField(choices=RSVP.STATUS_CHOICES)
   
    class Meta:
        model = RSVP
        fields = [
            'id', 'event', 'event_title', 'attendee', 'attendee_name', 
            'organizer_name', 'status', 'created_at'
        ]
        read_only_fields = ['attendee', 'created_at']

    def validate(self, data):
        try:
            request = self.context.get('request')
            if request and request.method == 'POST':
                event = data.get('event')
                attendee = request.user.attendee

                if not attendee:
                    raise serializers.ValidationError({
                        "error": "User is not registered as an attendee",
                        "code": "not_attendee"
                    })
                
                if RSVP.objects.filter(event=event, attendee=attendee).exists():
                    raise serializers.ValidationError({
                        "error": "You have already RSVP'd to this event",
                        "code": "duplicate_rsvp"
                    })
            return data
        except Exception as e:
            raise serializers.ValidationError({
                "error": "Validation failed",
                "code": "validation_error",
                "details": str(e)
            })
            raise