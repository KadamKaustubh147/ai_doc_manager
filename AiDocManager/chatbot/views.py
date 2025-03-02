from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import File, KeyEntity
import requests
import json
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.postgres.search import SearchVector





# Create your views here.

from allauth.socialaccount.models import SocialAccount




@login_required
def profile(request):
    # profile_pic_url = get_user_profile_picture(request.user)
    context = {}

    return render(request, 'profile.html', context)




API_URL = "https://commissioner-relations-priorities-standings.trycloudflare.com/upload/"


# @login_required
# def app(request):
#     # Get sorting, filtering, and search parameters from request
#     sort_by = request.GET.get("sort", "date")
#     order = request.GET.get("order", "desc")  # 'asc' or 'desc'
#     category_filter = request.GET.get("category", "")  # Category filter
#     search_query = request.GET.get("q", "").strip()  # Search input

#     # Define sorting options
#     sort_options = {
#         "date": "-uploaded_at" if order == "desc" else "uploaded_at",
#         "name": "-file" if order == "desc" else "file",
#         "category": "-document_type" if order == "desc" else "document_type",
#     }
    
#     sort_field = sort_options.get(sort_by, "-uploaded_at")
    
#     # Filter files by user
#     files = File.objects.filter(user=request.user)

#     # Apply category filter if selected
#     if category_filter:
#         files = files.filter(document_type=category_filter)
    
#     # Apply case-sensitive search filter on summary and additional_info fields
#     if search_query:
#         files = files.filter(
#             Q(summary__regex=rf".*{search_query}.*") | 
#             Q(additional_info__regex=rf".*{search_query}.*")
#         )

#     # Apply sorting
#     files = files.order_by(sort_field)

#     # Handle file upload
#     if request.method == "POST":
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_instance = form.save(commit=False)
#             file_instance.user = request.user
#             file_instance.save()

#             # Send the uploaded file to the external API
#             with open(file_instance.file.path, "rb") as f:
#                 response = requests.post(API_URL, files={"file": f})

#             print("API Response Status:", response.status_code)
#             print("Raw API Response Text:", response.text)

#             if response.status_code == 200:
#                 try:
#                     data = response.json()
#                     if isinstance(data, str):
#                         data = json.loads(data)
#                 except ValueError:
#                     print("Error: API response is not valid JSON:", response.text)
#                     return redirect("app")

#                 print("Parsed API Response:", data)

#                 if "document_type" in data or "summary" in data or "additional_info" in data:
#                     file_instance.document_type = data.get("document_type", "")
#                     file_instance.summary = data.get("summary", "")
#                     file_instance.additional_info = data.get("additional_info", "")
#                     file_instance.save()
#                 else:
#                     print("Warning: API did not return expected metadata fields!")

#                 key_entities = data.get("key_entities", [])
#                 if isinstance(key_entities, str):
#                     try:
#                         key_entities = json.loads(key_entities)
#                     except json.JSONDecodeError:
#                         print("Error: key_entities is not valid JSON:", key_entities)
#                         key_entities = []

#                 if isinstance(key_entities, list):  
#                     for entity in key_entities:
#                         if isinstance(entity, dict):  
#                             KeyEntity.objects.create(
#                                 file=file_instance,
#                                 name=entity.get("name", ""),
#                                 value=entity.get("value", ""),
#                                 entity_type=entity.get("type", ""),
#                             )
#                         else:
#                             print("Warning: Skipping invalid entity:", entity)
#                 else:
#                     print("Error: key_entities is not a list:", key_entities)
#     else:
#         form = FileUploadForm()

#     context = {
#         "form": form,
#         "files": files,
#         "sort": sort_by,
#         "order": order,
#         "category_filter": category_filter,
#         "search_query": search_query,
#         "categories": File.objects.values_list("document_type", flat=True).distinct(),
#     }
#     return render(request, "app.html", context)




@login_required
def app(request):
    # Get sorting, filtering, and search parameters from request
    sort_by = request.GET.get("sort", "date")
    order = request.GET.get("order", "desc")  # 'asc' or 'desc'
    category_filter = request.GET.get("category", "")  # Category filter
    search_query = request.GET.get("q", "").strip()  # Search input

    # Define sorting options
    sort_options = {
        "date": "-uploaded_at" if order == "desc" else "uploaded_at",
        "name": "-file" if order == "desc" else "file",
        "category": "-document_type" if order == "desc" else "document_type",
    }
    
    sort_field = sort_options.get(sort_by, "-uploaded_at")
    
    # Filter files by user
    files = File.objects.filter(user=request.user)

    # Apply category filter if selected
    if category_filter:
        files = files.filter(document_type=category_filter)
    
    # Apply case-insensitive search on summary and additional_info
    if search_query:
        files = files.filter(
            Q(summary__icontains=search_query) | 
            Q(additional_info__icontains=search_query)
        )        

    # Apply sorting
    files = files.order_by(sort_field)

    # Handle file upload
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()

            # Send the uploaded file to the external API
            with open(file_instance.file.path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            print("API Response Status:", response.status_code)
            print("Raw API Response Text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, str):
                        data = json.loads(data)
                except ValueError:
                    print("Error: API response is not valid JSON:", response.text)
                    return redirect("app")

                print("Parsed API Response:", data)

                if "document_type" in data or "summary" in data or "additional_info" in data:
                    file_instance.document_type = data.get("document_type", "")
                    file_instance.summary = data.get("summary", "")
                    file_instance.additional_info = data.get("additional_info", "")
                    file_instance.save()
                else:
                    print("Warning: API did not return expected metadata fields!")

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
        "files": files,
        "sort": sort_by,
        "order": order,
        "category_filter": category_filter,
        "search_query": search_query,
        "categories": File.objects.values_list("document_type", flat=True).distinct(),
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



