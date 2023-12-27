# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.db.models import F, Window, Sum
from django.db.models.functions import DenseRank
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

# Models
from users.models import Profile, Country
from demonlist.models import Demon, Record

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
        countries = Country.objects.all().order_by("country")
        records = Record.objects.filter(player=profile)

        context["countries"] = countries
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

        records = Record.objects.filter(player=user.profile, accepted=True).order_by("-datetime_submit")
        
        try:
            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
            )

            players_filtered = players_annotated.filter(user__username=user.profile)

            original_positions = {player.id: player.position for player in players_annotated}

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])

            ranking = original_positions[players_final[0].id]
        
        except:
            ranking = "-"


        try:    
            hardest = records.order_by("demon__position")[0].demon.level
        except:
            hardest = "-"


        context["following"] = following
        context["hardest"] = hardest
        context["ranking"] = ranking
        context["records"] = records
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        action = self.request.POST.get("action", None)

        print(self.request.user)

        if action == "follow":
            self.get_object().profile.followers.add(self.request.user.profile)
            self.request.user.profile.followings.add(user.profile)
        elif action == "unfollow":
            user.profile.followers.remove(Profile.objects.get(id=self.request.user.profile.id))
            self.request.user.profile.followings.remove(Profile.objects.get(id=user.profile.id))
        elif action == "delete":
            user.profile.picture.delete()

        
        return super().get(request, *args, **kwargs)
