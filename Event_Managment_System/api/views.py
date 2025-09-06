from rest_framework import generics, serializers, viewsets, permissions, status,exceptions
from .serializers import RegisterSerializer, EventSerializer, CategorySerializer, OrganizerSerializer, AttendeeSerializer, RSVPSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Event, Category, Organizer, Attendee, RSVP
from rest_framework.exceptions import ValidationError as DRFValidationError
from .permissions import IsOrganizer, IsAttendee
from rest_framework.permissions import AllowAny, IsAuthenticated   #to explicitly allow public (unauthenticated) access:  
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action

from rest_framework.views import APIView





User = get_user_model()

#----------------------------------------
# Base ViewSet with Common Functionality |
#----------------------------------------
class BaseViewSet(viewsets.ModelViewSet):
    
    #Base ViewSet with common error handling and permissions
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def handle_exception(self, exc):
    
        #Standard error handling for all API endpoints
        #Returns consistent error format across all ViewSets
        
        # Handle Django validation errors
        if isinstance(exc, DjangoValidationError):
            return Response(
                {
                    "error": str(exc),
                    "code": "validation_error",
                    "details": exc.message_dict if hasattr(exc, 'message_dict') else None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle DRF validation errors
        if isinstance(exc, DRFValidationError):
            return Response(
                {
                    "error": str(exc),
                    "code": "validation_error",
                    "details": exc.detail if hasattr(exc, 'detail') else None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle permission denied errors
        if isinstance(exc, exceptions.PermissionDenied):
            return Response(
                {
                    "error": "You do not have permission to perform this action",
                    "code": "permission_denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle authentication errors
        if isinstance(exc, exceptions.NotAuthenticated):
            return Response(
                {
                    "error": "Authentication credentials were not provided",
                    "code": "not_authenticated"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Handle not found errors
        if isinstance(exc, exceptions.NotFound):
            return Response(
                {
                    "error": "Resource not found",
                    "code": "not_found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Handle method not allowed
        if isinstance(exc, exceptions.MethodNotAllowed):
            return Response(
                {
                    "error": f"Method {self.request.method} not allowed",
                    "code": "method_not_allowed"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        # Default error handling
        return Response(
            {
                "error": "An unexpected error occurred",
                "code": "server_error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        #return super().handle_exception(exc)

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



    def perform_create(self, serializer):
        user = self.request.user
        # Check if organizer already exists for this user
        if Organizer.objects.filter(user=user).exists():
            raise DRFValidationError({
                "error": "User is already registered as an organizer",
                "code": "duplicate_organizer"
            })
        serializer.save(user=user)

class AttendeeCreateView(generics.CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Check if attendee already exists for this user
        if Attendee.objects.filter(user=user).exists():
            raise DRFValidationError({
                "error": "User is already registered as an attendee",
                "code": "duplicate_attendee"
            })
        serializer.save(user=user)



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
        # The attendee is automatically set in the serializer's validate method
        serializer.save()
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAttendee()]
        return super().get_permissions()