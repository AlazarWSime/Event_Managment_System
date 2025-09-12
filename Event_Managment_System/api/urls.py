from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, 
    protected_view, 
    OrganizerCreateView, 
    AttendeeCreateView, 
    EventViewSet, 
    CategoryViewSet, 
    RSVPViewSet,
    AttendeeViewSet
)

# Router and register viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet)  # Event creating route
router.register(r'categories', CategoryViewSet)
router.register(r'rsvps', RSVPViewSet, basename='rsvp')
router.register(r'attendees', AttendeeViewSet, basename='attendee')

urlpatterns = [
    # User management
    path('users/', RegisterView.as_view(), name='user-register'),
    path('organizers/', OrganizerCreateView.as_view(), name='organizer-create'),
    path('attendees/', AttendeeCreateView.as_view(), name='attendee-create'),
    
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Protected route
    path('protected/', protected_view, name='protected'),
    
    # Include router URLs
    path('', include(router.urls)),
]
