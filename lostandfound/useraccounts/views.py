from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import usecreationForm, userupdateForm
from django.urls import reverse_lazy

# Create your views here.

class registerView(CreateView):
    form_class = usecreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

class customloginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('landing')
    
class customlogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('landing')



