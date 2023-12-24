# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView, UpdateView

# Models
from users.models import Profile
from demonlist.models import Record

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
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    # Update profile view

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['country', 'youtube_channel']

    def get_object(self):
        # Return user's profile
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        records = Record.objects.filter(player=profile)

        context["records"] = records

        return context

    def get_success_url(self):
        # Return to user's profile
        username = self.object.user.username
        return reverse('users:detail', kwargs={"user": self.object.user.profile.id})
    
class UserDetailView(LoginRequiredMixin, DetailView):
    # User Detail View

    template_name = "users/detail.html"
    slug_field = "id"
    slug_url_kwarg = "user"
    queryset = User.objects.all()
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        # Add user's records to context
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["records"] = Record.objects.filter(player=user.profile, accepted=True).order_by("-datetime_submit")
        return context