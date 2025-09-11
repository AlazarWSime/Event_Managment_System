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
    RSVPViewSet
)

# Router and register viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'rsvps', RSVPViewSet, basename='rsvp')

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('organizer/register/', OrganizerCreateView.as_view(), name='organizer-register'),
    path('attendee/register/', AttendeeCreateView.as_view(), name='attendee-register'),
    path('protected/', protected_view, name='protected'),
    
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
