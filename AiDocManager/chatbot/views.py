from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

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

