from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import File, KeyEntity
import requests
import json


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




API_URL = "https://projectors-sleep-paid-findlaw.trycloudflare.com/upload/"

# def app(request):
#     files = None
#     if request.method == "POST":
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_instance = form.save(commit=False)
#             file_instance.user = request.user  # Link file to the user
#             file_instance.save()

#             # Send the uploaded file to the external API
#             with open(file_instance.file.path, "rb") as f:
#                 response = requests.post(API_URL, files={"file": f})

#             print("API Response Text:", response.text)  # Debugging line

#             if response.status_code == 200:
#                 try:
#                     data = response.json()  # Ensure response is parsed correctly
#                     if isinstance(data, str):  
#                         # If it's a string, attempt to convert it manually
#                         data = json.loads(data)
#                 except ValueError:
#                     print("Error: API response is not valid JSON:", response.text)
#                     return redirect("app")

#                 # Save extracted metadata in the File model
#                 file_instance.document_type = data.get("document_type", "")
#                 file_instance.summary = data.get("summary", "")
#                 file_instance.additional_info = data.get("additional_info", "")
#                 file_instance.save()

#                 # Save Key Entities in the KeyEntity model
#                 for entity in data.get("key_entities", []):
#                     KeyEntity.objects.create(
#                         file=file_instance,
#                         name=entity["name"],
#                         value=entity.get("value", ""),
#                         entity_type=entity.get("type", ""),
#                     )

#     else:
#         form = FileUploadForm()
#         files = File.objects.all().order_by("-uploaded_at")

#     context = {
#         "form": form,
#         "files": files
#     }
#     return render(request, "app.html", context)
import json
import requests

def app(request):
    files = File.objects.all().order_by("-uploaded_at")  # Ensure 'files' is always defined

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # Link file to the user
            file_instance.save()

            # Send the uploaded file to the external API
            with open(file_instance.file.path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            print("API Response Status:", response.status_code)  # Debugging line
            print("Raw API Response Text:", response.text)  # Debugging line

            if response.status_code == 200:
                try:
                    data = response.json()  # Try parsing JSON directly
                    if isinstance(data, str):  
                        # If API response is a string, convert manually
                        data = json.loads(data)

                except ValueError:
                    print("Error: API response is not valid JSON:", response.text)
                    return redirect("app")

                print("Parsed API Response:", data)  # Debugging line

                # Ensure API returned proper keys
                if "document_type" in data or "summary" in data or "additional_info" in data:
                    file_instance.document_type = data.get("document_type", "")
                    file_instance.summary = data.get("summary", "")
                    file_instance.additional_info = data.get("additional_info", "")
                    file_instance.save()
                else:
                    print("Warning: API did not return expected metadata fields!")

                # Ensure key_entities is a valid list
                key_entities = data.get("key_entities", [])
                if isinstance(key_entities, str):
                    try:
                        key_entities = json.loads(key_entities)
                    except json.JSONDecodeError:
                        print("Error: key_entities is not valid JSON:", key_entities)
                        key_entities = []

                if isinstance(key_entities, list):  
                    for entity in key_entities:
                        if isinstance(entity, dict):  
                            KeyEntity.objects.create(
                                file=file_instance,
                                name=entity.get("name", ""),
                                value=entity.get("value", ""),
                                entity_type=entity.get("type", ""),
                            )
                        else:
                            print("Warning: Skipping invalid entity:", entity)
                else:
                    print("Error: key_entities is not a list:", key_entities)

    else:
        form = FileUploadForm()

    context = {
        "form": form,
        "files": files  # 'files' is always defined now
    }
    return render(request, "app.html", context)




# take one more argument of file id
def file_details(request, file_id):
    
    files = File.objects.all().order_by("-uploaded_at")
    context = {
        "file": File.objects.filter(id=file_id).first()

    }
    
    if request.htmx:
        return render(request, 'file_details.html#sidebar', context)

    return render(request, 'file_details.html', context)



