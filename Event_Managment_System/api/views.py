from rest_framework import generics, serializers, viewsets, permissions, status
from .serializers import RegisterSerializer, EventSerializer, CategorySerializer, OrganizerSerializer, AttendeeSerializer, RSVPSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Event, Category, Organizer, Attendee, RSVP
from rest_framework.exceptions import ValidationError as DRFValidationError
from .permissions import IsOrganizer, IsAttendee
from rest_framework.permissions import AllowAny   #to explicitly allow public (unauthenticated) access:  
#from django.core.exceptions import ValidationError
from rest_framework.decorators import action

User = get_user_model()

#----------------------------------------
# Base ViewSet with Common Functionality |
#----------------------------------------
class BaseViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def handle_exception(self, exc):
        
        if isinstance(exc, DRFValidationError):
            return Response(
                {"error": str(exc), "code": "validation_error"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)

#--------------------------------
# Existing Views (Keep as is)    |
#--------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # 👈 This line is critical
#custom class-based view for user registration


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You have access because you're authenticated!"})

class OrganizerCreateView(generics.CreateAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="rsvps")
    def event_rsvps(self, request, pk=None):
      event = self.get_object()
      rsvps = RSVP.objects.filter(event=event)
      serializer = RSVPSerializer(rsvps, many=True)
      return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AttendeeCreateView(generics.CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#----------------------------------------
#  ViewSets now inherit from BaseViewSet |
#----------------------------------------
class EventViewSet(BaseViewSet):  #inherits from BaseViewSet
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    

    def perform_create(self, serializer):
        organizer = self.request.user.organizer
        serializer.save(organizer=organizer)
        
    def get_queryset(self):
        return Event.objects.all().order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['update','partial_update', 'destroy']:
            return [IsOrganizer()]
        return super().get_permissions()

class CategoryViewSet(BaseViewSet):  #inherits from BaseViewSet
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    pagination_class = None

class RSVPViewSet(BaseViewSet):
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # If user is an organizer, show RSVPs for all their events
        if hasattr(user, 'organizer'):
            organized_events = Event.objects.filter(organizer__user=user)
            return RSVP.objects.filter(event__in=organized_events)
        
        # If user is an attendee, show only their own RSVPs
        elif hasattr(user, 'attendee'):
            return RSVP.objects.filter(attendee__user=user)
        
        # Fallback for other users (admin/staff)
        return RSVP.objects.all()

    def perform_create(self, serializer):
        # Only attendees can create RSVPs
        if not hasattr(self.request.user, 'attendee'):
            raise DRFValidationError("Only attendees can create RSVPs")
        
        attendee = self.request.user.attendee
        serializer.save(attendee=attendee)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAttendee()]
        return super().get_permissions()