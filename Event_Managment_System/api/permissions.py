# api/permissions.py

from rest_framework import permissions

class IsOrganizer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.organizer.user == request.user
#Only the user who created this event can modify it


class IsAttendee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.attendee.user == request.user
 #Only the user who created this RSVP can modify it   
    