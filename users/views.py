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
    fields = ['country', 'youtube_channel', 'picture']

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
        user = self.object.user
        user.username = self.request.POST.get("username")
        user.save()
        return reverse('users:detail', kwargs={"user": self.object.user.id})
    
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
        following = self.request.user.profile.followings.all()
        if user.profile in following:
            following = True
        else:
            following = False
        context["following"] = following
        context["records"] = Record.objects.filter(player=user.profile, accepted=True).order_by("-datetime_submit")
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        action = self.request.POST.get("action", None)

        print(self.request.user)

        if action == "follow":
            self.get_object().profile.followers.add(self.request.user.profile)
            self.request.user.profile.followings.add(user.profile)
        else:
            user.profile.followers.remove(Profile.objects.get(id=self.request.user.profile.id))
            self.request.user.profile.followings.remove(Profile.objects.get(id=user.profile.id))

        
        return super().get(request, *args, **kwargs)
