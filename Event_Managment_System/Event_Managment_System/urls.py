#project/urls.py

"""
URL configuration for Event_Managment_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to the Event Management System API',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'api_redoc': '/api/redoc/',
            'auth': {
                'token_obtain': '/api/token/',
                'token_refresh': '/api/token/refresh/'
            },
            'users': {
                'register': '/api/users/',
                'organizers': '/api/organizers/',
                'attendees': '/api/attendees/'
            },
            'resources': {
                'events': '/api/events/',
                'categories': '/api/categories/',
                'rsvps': '/api/rsvps/'
            }
        }
    })

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API Root - Shows all available endpoints
    path('api/', api_root, name='api-root'),
    
    # Include API endpoints from the api app
    path('api/', include('api.urls')),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # DRF authentication (for browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]




