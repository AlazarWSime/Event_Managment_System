#views.py

from rest_framework import generics, serializers,viewsets, permissions
from .serializers import RegisterSerializer, EventSerializer, CategorySerializer, OrganizerSerializer, AttendeeSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Event, Category, Organizer, Attendee
from rest_framework.exceptions import ValidationError





User = get_user_model()
        
        
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You have access because you're autherticated!"})
    # Create your views here.


#-------------------------
# Organizer Views
#-------------------------

class OrganizerCreateView(generics.CreateAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#-------------------------
# Attendies Views
#-------------------------
class AttendeeCreateView(generics.CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)