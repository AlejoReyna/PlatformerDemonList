# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import F, Window, Sum
from django.db.models.functions import Rank
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView, TemplateView

# Models
from users.models import Profile, Country
from demonlist.models import Demon, Record

# Forms
from users.forms import SignupForm

# Functions
from demonlist import functions

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
    
class UpdateProfileView(LoginRequiredMixin, TemplateView):
    # Update profile view

    template_name = 'users/update_profile.html'

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

    def post(self, request, *args, **kwargs):
        # Return to user's profile
        user = self.request.user
        error_message = None
        try:
            if not(self.request.user.username == self.request.POST.get("username")):
                u = User.objects.get(username=self.request.POST.get("username"))
                error_message = "The username is already in use. Please choose another."
            else:
                user.username = self.request.POST.get("username")
                user.save()
        except:
            user.username = self.request.POST.get("username")
            user.save()
        profile = user.profile
        try:
            picture = self.request.FILES["picture"]
            file_path = default_storage.save(f"users/pictures/{profile.id}/{picture.name}", ContentFile(picture.read()))
            profile.picture = file_path
        except:
            pass
        try:
            country = Country.objects.get(country=self.request.POST.get("country"))
            profile.country = Country.objects.get(country=country)
        except:
            pass
        if not(self.request.POST.get("youtube_channel") == "https://www.youtube.com/@"):
            profile.youtube_channel = self.request.POST.get("youtube_channel")
        else:
            profile.youtube_channel = ""
        if not(self.request.POST.get("twitter") == "https://twitter.com/"):
            profile.twitter = self.request.POST.get("twitter")
        else:
            profile.twitter = ""
        if not(self.request.POST.get("twitch") == "https://twitch.tv/"):
            profile.twitch = self.request.POST.get("twitch")
        else:
            profile.twitch = ""
        if not(self.request.POST.get("facebook") == "https://facebook.com/"):
            profile.facebook = self.request.POST.get("facebook")
        else:
            profile.facebook = ""
        if self.request.POST.get("discord") != '' and self.request.POST.get("discord") != profile.discord:
            profile.discord = self.request.POST.get("discord")
            profile.verified = None
        profile.save()

        functions.update_countries_list_points(profile.country)
        countries = Country.objects.all().order_by("country")
        records = Record.objects.filter(player=profile)

        return render(
        request,
        'users/update_profile.html',
        {'error_message': error_message, 'countries': countries, 'records': records}
    )

class RecordsStatusView(LoginRequiredMixin, TemplateView):
    # Records status view

    template_name = 'users/records_status.html'

    def get_object(self):
        # Return user's profile
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        records = Record.objects.filter(player=profile)

        context["records"] = records
        return context
    
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

        records = Record.objects.filter(player=user.profile, accepted=True).order_by("demon__position")
        
        try:
            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=Rank(), order_by=F('list_points').desc())
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
        search_user = self.request.POST.get("user", None)
        option = self.request.POST.get("option", None)


        if action:
            if action == "follow":
                self.get_object().profile.followers.add(self.request.user.profile)
                self.request.user.profile.followings.add(user.profile)
            elif action == "unfollow":
                user.profile.followers.remove(Profile.objects.get(id=self.request.user.profile.id))
                self.request.user.profile.followings.remove(Profile.objects.get(id=user.profile.id))
            elif action == "delete":
                user.profile.picture.delete()
            return super().get(request, *args, **kwargs)
        elif user:
            print(search_user)
            print(option)
            print(user.profile.followings.all())
            if search_user == "":
                if option == "followers":
                    users = user.profile.followers.all()
                elif option == "following":
                    users = user.profile.followings.all()
                print(users)
                users = list(users.values("user__id", "picture", "user__username"))
            else:
                if option == "followers":
                    users = user.profile.followers.filter(user__username__icontains=search_user)
                elif option == "following":
                    users = user.profile.followings.filter(user__username__icontains=search_user)
                print(users)
                users = list(users.values("user__id", "picture", "user__username"))
                print(users)
            return JsonResponse(users, safe=False)
        
class UserDetailView2(LoginRequiredMixin, DetailView):
    # User Detail View with username in the URL

    template_name = "users/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"
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

        records = Record.objects.filter(player=user.profile, accepted=True).order_by("demon__position")
        
        try:
            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=Rank(), order_by=F('list_points').desc())
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
        search_user = self.request.POST.get("user", None)
        option = self.request.POST.get("option", None)


        if action:
            if action == "follow":
                self.get_object().profile.followers.add(self.request.user.profile)
                self.request.user.profile.followings.add(user.profile)
            elif action == "unfollow":
                user.profile.followers.remove(Profile.objects.get(id=self.request.user.profile.id))
                self.request.user.profile.followings.remove(Profile.objects.get(id=user.profile.id))
            elif action == "delete":
                user.profile.picture.delete()
            return super().get(request, *args, **kwargs)
        elif user:
            print(search_user)
            print(option)
            print(user.profile.followings.all())
            if search_user == "":
                if option == "followers":
                    users = user.profile.followers.all()
                elif option == "following":
                    users = user.profile.followings.all()
                print(users)
                users = list(users.values("user__id", "picture", "user__username"))
            else:
                if option == "followers":
                    users = user.profile.followers.filter(user__username__icontains=search_user)
                elif option == "following":
                    users = user.profile.followings.filter(user__username__icontains=search_user)
                print(users)
                users = list(users.values("user__id", "picture", "user__username"))
                print(users)
            return JsonResponse(users, safe=False)
        
