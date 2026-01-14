import time
from django.shortcuts import render, HttpResponse, redirect
from allauth.account.views import SignupView, LoginView, PasswordResetView, PasswordResetDoneView
from django.template.loader import render_to_string
from django.urls import reverse_lazy


# Create your views here.





def home(request):
    return render(request, 'landing.html')

def custom404(request, exception):
    return render(request, '404.html', status=404)


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        start_time = time.time()

        if request.htmx:
            print("htmx")
            html = render_to_string("account/login.html#htmx_login", request=request)
            print(f"View Execution Time: {time.time() - start_time:.3f} seconds")   
            return render(request, "account/login.html#htmx_login")
            # response = HttpResponse("Test Response")

            # return HttpResponse(html)
            # return HttpResponse(response)
        else:
            print('rendering og')
            print(f"View Execution Time: {time.time() - start_time:.3f} seconds")   
            return redirect('home')
        


    

class CustomSignupView(SignupView):
    def get(self, request, *args, **kwargs):
        if request.htmx:
            print("htmx")
            return render(request, "account/signup.html#htmx_signup")
        print('rendering og')

        return redirect('home')

        
        
class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html#htmx_password_reset"  # Your custom Tailwind template
    success_url = reverse_lazy("account_reset_password_done")  # Redirect after form submission

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"
    def get(self, request, *args, **kwargs):
        if request.htmx:
            print("htmx")
            return render(request, "account/password_reset_done.html#htmx_password_reset ")
        print('rendering og')

        return render(request, "account/password_reset_done.html")