from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
import os
import json
from django.shortcuts import redirect
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from decouple import config

# Load Google Scopes from .env
SCOPES = config("SCOPES")
CLIENT_ID = config("DRIVE_CLIENT_ID")
CLIENT_SECRET = config("DRIVE_CLIENT_SECRET")
REDIRECT_URI = config("DRIVE_REDIRECT_URI")

# Create your views here.

from allauth.socialaccount.models import SocialAccount

def get_user_profile_picture(user):
    try:
        # Get the social account for this user
        social_account = SocialAccount.objects.get(user=user, provider='google')
        
        # The extra_data field contains the OAuth response data
        extra_data = social_account.extra_data
        
        # Google stores the profile picture URL in the 'picture' field
        if 'picture' in extra_data:
            return extra_data['picture']
    except SocialAccount.DoesNotExist:
        pass
    
    return None  # Return a default if no Google account or no picture

def profile(request):
    profile_pic_url = get_user_profile_picture(request.user)
    context = {
        "pfp": profile_pic_url
    }
    return render(request, 'profile.html', context)



@login_required
def connect_google_drive(request):
    """ Initiates OAuth flow to connect user's Google Drive. """
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return redirect(auth_url)


@login_required
def google_drive_callback(request):
    """ Handles Google's OAuth callback and stores credentials. """
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session["google_drive_credentials"] = json.loads(credentials.to_json())

    return redirect("/app/profile")  # Redirect to profile page after connecting



# @login_required
# def list_google_drive_files(request):
#     """ Fetches and displays user's Google Drive files. """
#     creds_data = request.session.get("google_drive_credentials")

#     if not creds_data:
#         return redirect("connect_google_drive")

#     creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
#     service = build("drive", "v3", credentials=creds)
    
#     results = service.files().list(pageSize=10, fields="files(id, name)").execute()
#     files = results.get("files", [])

#     return render(request, "drive_files.html", {"files": files})