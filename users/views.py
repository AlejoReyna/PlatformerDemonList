# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView, UpdateView

# Models
from users.models import Profile

class LoginView(auth_views.LoginView):
    # Login View

    template_name = "users/login.html"
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    # Vista de Logout
     
    pass