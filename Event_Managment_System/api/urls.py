#app/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, protected_view, OrganizerCreateView, AttendeeCreateView


urlpatterns = [
    path('users/', RegisterView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('organizers/', OrganizerCreateView.as_view(), name='organizer-create'),
    path('attendees/', AttendeeCreateView.as_view(), name='attendee-create'),
    path('protected/', protected_view, name = 'protected'),
]
