from django.contrib import admin
from django.urls import path, include

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentification.urls')),
    path('api/', include('myapi.urls')),  # This will make your myapi routes available at /api/
]


