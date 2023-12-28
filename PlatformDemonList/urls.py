"""PlatformDemonList URLs module."""

# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponsePermanentRedirect
from django.urls import path, re_path, include

# Views
from PlatformDemonList import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include(('demonlist.urls', 'demonlist'), namespace='demonlist')),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path('accounts/', include('allauth.urls')),

    path(
        route='guidelines/',
        view=views.GuidelinesView.as_view(),
        name='guidelines'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
