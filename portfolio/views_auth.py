from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

class CumbiaLoginView(LoginView):
    template_name = 'portfolio/login.html'
    redirect_authenticated_user = True
    extra_context = {'segment': 'auth'}

def cumbia_logout(request):
    logout(request)
    return redirect('portfolio:index')
