from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Event, Category, Organizer, Attendee # import my event and category from models.py

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
    organizer = serializers.ReadOnlyField(source='organizer.organization_name')
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'organizer', 'categories', 'start_date', 'end_date']


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
            'organization': {'required': True}
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