
from django.urls import path, include
from . import views
# from .views import connect_google_drive, google_drive_callback


urlpatterns = [
    path("", views.app, name="app"),
    path("profile", views.profile, name="profile"),
    # path("google-drive/connect/", connect_google_drive, name="connect_google_drive"),
    # path("google-drive-callback/", google_drive_callback, name="google_drive_callback"),
]
