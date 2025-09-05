#admin.py

from django.contrib import admin
from .models import User, Organizer, Attendee, Category, Event, EventCategory, RSVP

#--------------------------------------------------
# User Admin
#--------------------------------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

#--------------------------------------------------
# Organizer Admin
#--------------------------------------------------
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'bio_preview')
    list_filter = ('organization_name',)
    search_fields = ('user__username', 'organization_name')
    raw_id_fields = ('user',)
    
    def bio_preview(self, obj):
        return obj.bio[:50] + '...' if obj.bio else 'No bio'
    bio_preview.short_description = 'Bio Preview'

#--------------------------------------------------
# Attendee Admin
#--------------------------------------------------
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'user_email')
    list_filter = ('company',)
    search_fields = ('user__username', 'company')
    raw_id_fields = ('user',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

#--------------------------------------------------
# Category Admin
#--------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_count')
    search_fields = ('name',)
    
    def event_count(self, obj):
        return obj.event_set.count()
    event_count.short_description = 'Events Count'

#--------------------------------------------------
# Event Admin
#--------------------------------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'location', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date', 'created_at', 'categories')
    search_fields = ('title', 'description', 'location', 'organizer__organization_name')
    raw_id_fields = ('organizer', 'categories')
    date_hierarchy = 'start_date'
   

#--------------------------------------------------
# EventCategory Admin (Through model)
#--------------------------------------------------
@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'category')
    list_filter = ('category',)
    search_fields = ('event__title', 'category__name')

#--------------------------------------------------
# RSVP Admin
#--------------------------------------------------
@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('event__title', 'attendee__user__username')
    raw_id_fields = ('event', 'attendee')