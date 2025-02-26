from django.shortcuts import render
from allauth.account.views import SignupView, LoginView
# Create your views here.

def home(request):
    return render(request, 'landing.html')

def custom404(request, exception):
    return render(request, '404.html', status=404)

# def CustomSignupView(SignupView):
#     def get(self, request, *args, **kwargs):
#         if request.htmx:
#             return render(request, "account/signup.html#htmx_signup")
#         # return super().get(request, *args, **kwargs)
#         return render(request, "account/signup.html")

def CustomSignupView(SignupView):
    def get(self,request,*args, **kwargs):
        if request.htmx:
            self.template_name = "account/signup.html#htmx_signup"
            return render(request, "account/signup.html#htmx_signup")
        # return super().get(request, *args, **kwargs)
        return render(request, "account/signup.html")

def hello(request):
    render(request, 'hello.html')