"""
URL configuration for AiDocManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from . import views
from django.conf.urls import handler404
from .views import custom404
from allauth.account.views import LoginView

handler404 = custom404
import pdb

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.home, name="home"),
    path("idk/", include("chatbot.urls")),
    # pdb.set_trace(),
    path('accounts/signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='account_login'),
    path('accounts/', include('allauth.urls')),  # Django Allauth URLs
]
