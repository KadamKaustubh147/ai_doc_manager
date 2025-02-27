from django.shortcuts import render
from allauth.account.views import SignupView, LoginView
# Create your views here.

def home(request):
    return render(request, 'landing.html')

def custom404(request, exception):
    return render(request, '404.html', status=404)


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.htmx:
            print("htmx")
            return render(request, "account/login.html#htmx_login")
        print('rendering og')
        return render(request, "account/login.html")
    

class CustomSignupView(SignupView):
    def get(self, request, *args, **kwargs):
        if request.htmx:
            print("htmx")
            return render(request, "account/signup.html#htmx_signup")
        print('rendering og')
        return render(request, "account/signup.html")
    