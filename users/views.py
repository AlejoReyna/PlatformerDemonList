# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView, UpdateView

# Models
from users.models import Profile

# Forms
from users.forms import SignupForm

class LoginView(auth_views.LoginView):
    # Login View

    template_name = "users/login.html"
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    # Vista de Logout
     
    pass

class SignupView(FormView):
    # Users sign up view

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Save form data
        form.save()
        return super().form_valid(form)