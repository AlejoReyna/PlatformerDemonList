"""Demon List views."""

# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db.models import F, Window, Sum, Case, When, CharField, Value, ExpressionWrapper, Func, IntegerField
from django.db.models.functions import Rank, Cast
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

# Models
from django.contrib.auth.models import User
from demonlist.models import Demon, Record, Changelog
from users.models import Profile, Country

# Functions
from demonlist import functions

# Utils
import datetime
import os

class ModeradorMixin(UserPassesTestMixin):
    def test_func(self):
        is_mod = False
        if str(self.request.user.groups.get()) == "Mod":
            is_mod = True
        return self.request.user.is_authenticated and is_mod

class ListHelperMixin(UserPassesTestMixin):
    def test_func(self):
        is_helper = False
        if str(self.request.user.groups.get()) == "Mod" or str(self.request.user.groups.get()) == "List Helper":
            is_helper = True
        return self.request.user.is_authenticated and is_helper

class DemonListView(ListView):
    """Return all list demons."""

    template_name = 'demonlist/list.html'
    model = Demon
    ordering = ('position',)
    paginate_by = 30
    context_object_name = 'demons'

class DemonDetailView(DetailView):
    # Return demon detail
    template_name = "demonlist/detail.html"
    queryset = Demon.objects.all()
    slug_field = 'position'
    slug_url_kwarg = 'position'
    context_object_name = "demon"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        demon = self.get_object()
        changelog = Changelog.objects.filter(demon=demon)
        records = Record.objects.filter(demon=demon, accepted=True)

        context["changelog"] = changelog
        context["records"] = records
        return context

    def post(self, request, position):
        r = request.POST
        demon = self.get_object()
        option = r.get("option", None)

        if option == "best_time":
            records = Record.objects.filter(demon=demon, accepted=True).order_by("best_time")

            records = list(records.annotate(video_platform=Case(
                When(video__regex=r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/.+', then=Value('YouTube')),
                When(video__regex=r'(https?://)?(www\.)?twitch\.(tv|com)/.+', then=Value('Twitch')),
                When(video__regex=r'(https?://)?clips\.twitch\.tv/.+', then=Value('Twitch')),
                When(video__regex=r'(https?://)?(www\.)?facebook\.(com)/.+', then=Value('Facebook')),
                When(video__regex=r'(https?://)?drive\.google\.com/.+', then=Value('Drive')),

            default=Value(''),
            output_field=CharField())).values("player__user__id", "player__user__username", "player__country__picture", "player__country__country", "video", "best_time", "video_platform"))

            return JsonResponse(records, safe=False)
        
        elif option == "order":
            records = Record.objects.filter(demon=demon, accepted=True)

            records = list(records.annotate(video_platform=Case(
            When(video__regex=r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/.+', then=Value('YouTube')),
            When(video__regex=r'(https?://)?(www\.)?twitch\.(tv|com)/.+', then=Value('Twitch')),
            When(video__regex=r'(https?://)?clips\.twitch\.tv/.+', then=Value('Twitch')),
            When(video__regex=r'(https?://)?(www\.)?facebook\.(com)/.+', then=Value('Facebook')),
            When(video__regex=r'(https?://)?drive\.google\.com/.+', then=Value('Drive')),
            default=Value(''),
            output_field=CharField())).values("player__user__id", "player__user__username", "player__country__picture", "player__country__country", "video", "best_time", "video_platform"))

            return JsonResponse(records, safe=False)


class SubmitRecordView(TemplateView):
    """Submit a new record."""

    template_name = 'demonlist/submit_record.html'
    success_url = reverse_lazy('demonlist:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        demons = Demon.objects.all()

        context['user'] = self.request.user
        context['demons'] = demons
        return context

    def post(self, request):
        r = request.POST
        demon = r.get("demon", None)
        hours = r.get("hours", None)
        minutes = r.get("minutes", None)
        seconds = r.get("seconds", None)
        milliseconds = r.get("milliseconds", None)
        profile = r.get("profile", None)
        video = r.get("video", None)
        raw_footage = r.get("raw_footage", None)
        notes = r.get("notes", None)

        time = datetime.time(int(hours), int(minutes), int(seconds), int(milliseconds) * 1000)
        
        print(r)

        Record.objects.create(demon=Demon.objects.get(level=demon),
                            best_time=time,
                            player=Profile.objects.get(id=profile),
                            video=video,
                            raw_footage=raw_footage,
                            notes=notes,
                            )
        
        return HttpResponseRedirect(reverse_lazy('demonlist:list'))
        
class StatsViewerView(TemplateView):
    # Return stats viewer view
    template_name = "demonlist/stats_viewer.html"
    success_url = reverse_lazy('demonlist:stats_viewer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = Profile.objects.filter(list_points__gte=1).annotate(position=Window(expression=Rank(), order_by=F('list_points').desc()))
        countries = Country.objects.all().order_by("country")

        if (players.count() % 50) == 0:
            pages_records_max = players.count() // 50
        else:
            pages_records_max = players.count() // 50 + 1

        context["countries"] = countries
        context["pages_records"] = 1
        context["pages_records_max"] = pages_records_max
        context["players"] = players[:50]
        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("player", None) or r.get("player", None) == "":

            print("aver esto")

            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=Rank(), order_by=F('list_points').desc())
            )

            if r.get("select_country", None):
                players_filtered = players_annotated.filter(user__username__icontains=r.get("player", None), country__country=r.get("select_country", None))
            else:
                players_filtered = players_annotated.filter(user__username__icontains=r.get("player", None))

            print("aver esto2")

            original_positions = {player.id: player.position for player in players_annotated}

            print("aver esto3")

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])
            print("aver esto4")
                
            result_list = [
                {
                    'id': player.id,
                    'user__id': player.user.id,
                    'user__username': player.user.username,
                    'list_points': player.list_points,
                    'position': original_positions[player.id],
                    'country__picture': player.country.picture.url if player.country else "",
                    'country__country': player.country.country if player.country else ""
                }
                for player in players_final
            ]
            print("aver esto5")

            if (len(result_list) % 50) == 0:
                pages_records_max = len(result_list) // 50
            else:
                pages_records_max = len(result_list) // 50 + 1
                    
            if r.get("pages_records"):
                page_min = (int(request.POST.get("pages_records")) - 1) * 50
                page_max = int(request.POST.get("pages_records")) * 50
                result_list = result_list[page_min:page_max]
                reset_pages = False
            else:
                result_list = result_list[:50]
                reset_pages = True

            result_list = [result_list, reset_pages, pages_records_max]
            print("aver esto6")

            return JsonResponse(result_list, safe=False)
        
        if r.get("country", None) or r.get("country", None) == "":
            
            countries_annotated = Country.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=Rank(), order_by=F('list_points').desc())
            )

            countries_filtered = countries_annotated.filter(country__icontains=r.get("country", None))

            original_positions = {country.id: country.position for country in countries_annotated}

            countries_final = sorted(countries_filtered, key=lambda country: original_positions[country.id])

            result_list = [
                {
                    'id': country.id,
                    'country': country.country,
                    'picture': country.picture.url,
                    'position': original_positions[country.id],
                    'list_points': country.list_points,
                }
                for country in countries_final
            ]

            if (len(result_list) % 50) == 0:
                pages_records_max = len(result_list) // 50
            else:
                pages_records_max = len(result_list) // 50 + 1

            if r.get("pages_records"):
                page_min = (int(request.POST.get("pages_records")) - 1) * 50
                page_max = int(request.POST.get("pages_records")) * 50
                result_list = result_list[page_min:page_max]
                reset_pages = False
            else:
                result_list = result_list[:50]
                reset_pages = True

            result_list = [result_list, reset_pages, pages_records_max]

            return JsonResponse(result_list, safe=False)
        
        if r.get("option", None):
            
            if r.get("option", None) == "Nations":

                countries = Country.objects.filter(list_points__gte=1).annotate(position=Window(expression=Rank(), order_by=F('list_points').desc()))

                if (len(countries) % 50) == 0:
                    pages_records_max = len(countries) // 50
                else:
                    pages_records_max = len(countries) // 50 + 1

                if r.get("pages_records"):
                    page_min = (int(request.POST.get("pages_records")) - 1) * 50
                    page_max = int(request.POST.get("pages_records")) * 50
                    countries = list(countries.values("id", "picture", "list_points", "position", "country"))[page_min:page_max]
                    reset_pages = False
                else:
                    countries = list(countries.values("id", "picture", "list_points", "position", "country"))[:50]
                    reset_pages = True

                countries = [countries, reset_pages, pages_records_max]

                return JsonResponse(countries, safe=False)
            
            elif r.get("option", None) == "Individual":
                players = Profile.objects.filter(list_points__gte=1).annotate(position=Window(expression=Rank(), order_by=F('list_points').desc()))

                if (len(players) % 50) == 0:
                    pages_records_max = len(players) // 50
                else:
                    pages_records_max = len(players) // 50 + 1

                if r.get("pages_records"):
                    page_min = (int(request.POST.get("pages_records")) - 1) * 50
                    page_max = int(request.POST.get("pages_records")) * 50
                    players = list(players.values("id", "user__id", "user__username", "list_points", "position", "country__picture", "country__country"))[page_min:page_max]
                    reset_pages = False
                else:
                    players = list(players.values("id", "user__id", "user__username", "list_points", "position", "country__picture", "country__country"))[:50]
                    reset_pages = True

                players = [players, reset_pages, pages_records_max]

                return JsonResponse(players, safe=False)

        if r.get("select_country", None) or r.get("select_country", None) == "":
            
            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=Rank(), order_by=F('list_points').desc())
            )

            if r.get("select_country", None):
                players_filtered = players_annotated.filter(country__country=r.get("select_country", None))
            else:
                players_filtered = players_annotated

            original_positions = {player.id: player.position for player in players_annotated}

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])

            result_list = []
            for player in players_final:
                if player.country:
                    picture_url = player.country.picture.url
                    country = player.country.country
                else:
                    picture_url = ""
                    country = ""

                result_list.append({
                        'id': player.id,
                        'user__id': player.user.id,
                        'user__username': player.user.username,
                        'list_points': player.list_points,
                        'position': original_positions[player.id],
                        'country__picture': picture_url,
                        'country__country': country,
                    })

            if (len(result_list) % 50) == 0:
                pages_records_max = len(result_list) // 50
            else:
                pages_records_max = len(result_list) // 50 + 1

            if r.get("pages_records"):
                page_min = (int(request.POST.get("pages_records")) - 1) * 50
                page_max = int(request.POST.get("pages_records")) * 50
                result_list = result_list[page_min:page_max]
                reset_pages = False
            else:
                result_list = result_list[:50]
                reset_pages = True

            print(result_list)
            result_list = [result_list, reset_pages, pages_records_max]

            print(pages_records_max)

            return JsonResponse(result_list, safe=False)

class CheckRecordsView(LoginRequiredMixin, ListHelperMixin, TemplateView):
    # Return check records view
    template_name = "demonlist/check_records.html"
    success_url = reverse_lazy('demonlist:check_records')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(self.request.user.groups.get())
        if str(self.request.user.groups.get()) == "List Helper":
            records = Record.objects.filter(accepted=None).exclude(player__user__username="GuitarHeroStyles")
        else:
            records = Record.objects.filter(accepted=None)
        context["records"] = records
        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("status", None):
            if r.get("status", None) == "Pending":
                records = Record.objects.filter(accepted=None)
            elif r.get("status", None) == "Canceled":
                records = Record.objects.filter(accepted=False)
            elif r.get("status", None) == "Accepted":
                records = Record.objects.filter(accepted=True)

            if str(self.request.user.groups.get()) == "List Helper":
                records = records.exclude(player__user__username="GuitarHeroStyles")

            records = list(records.values("id", "best_time", "player__user__username", "player__user__id", "demon__level", "video", "raw_footage", "notes", "mod_notes"))
            return JsonResponse(records, safe=False)
        
        if r.get("accept_id", None):
            record = Record.objects.get(id=r.get("accept_id", None))
            mod_notes = r.get("mod_notes", None)
            hours = r.get("hours", None)
            minutes = r.get("minutes", None)
            seconds = r.get("seconds", None)
            milliseconds = r.get("milliseconds", None)

            time = datetime.time(int(hours), int(minutes), int(seconds), int(milliseconds[:3]) * 1000)

            try:
                old_record = Record.objects.get(demon=record.demon, player=record.player, accepted=True)
                old_record.best_time = time
                old_record.video = record.video
                old_record.raw_footage = record.raw_footage
                old_record.notes = record.notes
                old_record.mod_notes = mod_notes
                old_record.mod = self.request.user.profile
                old_record.datetime_accepted = datetime.datetime.now()
                old_record.save()
                if record.accepted == None:
                    record.delete()
            except:
                record.best_time = time
                record.accepted = True
                record.mod_notes = mod_notes
                record.mod = self.request.user.profile
                record.datetime_accepted = datetime.datetime.now()
                record.save()

            functions.update_top_order(record.demon)
            functions.update_top_best_time(record.demon)
            functions.update_players_list_points(record.player)
            functions.update_countries_list_points(record.player.country)

            return JsonResponse(record.id, safe=False)
        
        if r.get("cancel_id", None):
            record = Record.objects.get(id=r.get("cancel_id", None))
            mod_notes = r.get("mod_notes", None)

            if record.accepted:

                functions.update_top_order(record.demon)
                functions.update_top_best_time(record.demon)
                functions.update_players_list_points(record.player)
                functions.update_countries_list_points(record.player.country)

            record.accepted = False
            record.mod_notes = mod_notes
            record.mod = self.request.user.profile
            record.save()

            return JsonResponse(record.id, safe=False)
        
class CheckVerificationsView(LoginRequiredMixin, ModeradorMixin, TemplateView):
    # Return check verifications view
    template_name = "demonlist/check_verifications.html"
    success_url = reverse_lazy('demonlist:check_verifications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.filter(discord__isnull=False, verified=None)

        context["profiles"] = profiles

        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("status", None):
            if r.get("status", None) == "Pending":
                profiles = Profile.objects.filter(discord__isnull=False, verified=None)
            elif r.get("status", None) == "Canceled":
                profiles = Profile.objects.filter(discord__isnull=False, verified=False)
            elif r.get("status", None) == "Verified":
                profiles = Profile.objects.filter(discord__isnull=False, verified=True)

            profiles = list(profiles.values("id", "user__username", "discord"))
            return JsonResponse(profiles, safe=False)
        
        if r.get("accept_id", None):
            profile = Profile.objects.get(id=r.get("accept_id", None))

            profile.verified = True
            profile.save()

            return JsonResponse(profile.id, safe=False)
        
        if r.get("cancel_id", None):
            profile = Profile.objects.get(id=r.get("cancel_id", None))

            profile.verified = False
            profile.save()

            return JsonResponse(profile.id, safe=False)

class AddEditDemonView(LoginRequiredMixin, ModeradorMixin, TemplateView):
    # Return add edit demon view
    template_name = "demonlist/add_edit_demon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        demons = Demon.objects.all()

        context["demons"] = demons

        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("option", None) == "Add":
            level = r.get("add_demon", None)
            photo = request.FILES["photo"]
            position = r.get("position", None)
            creator = r.get("creator", None)
            verificator = r.get("verificator", None)
            verification_video = r.get("verification_video", None)
            level_id = r.get("level_id", None)
            object_count = r.get("object_count", None)
            demon_difficulty = r.get("demon_difficulty", None)
            level_password = r.get("level_password", None)

            demons = Demon.objects.filter(position__gte=position)
            for demon in demons:
                Changelog.objects.create(demon=demon,
                            reason=f"{level} was added above",
                            position=demon.position + 1,
                            change_number=1,
                            change_type="Down"
                            )
                demon.position += 1
                demon.save()

            if verification_video[:16] == "https://youtu.be":
                verification_video_embed = 'https://www.youtube.com/embed/' + verification_video.split('/')[3]
            elif verification_video[:29] == "https://www.youtube.com/watch":
                verification_video_embed = 'https://www.youtube.com/embed/' + verification_video.split('=')[1]
            else:
                verification_video_embed = None

            new_demon = Demon.objects.create(level=level,
                                photo=photo,
                                position=position,
                                creator=creator,
                                verificator=verificator,
                                verification_video=verification_video,
                                verification_video_embed=verification_video_embed,
                                level_id=level_id,
                                object_count=object_count,
                                demon_difficulty=demon_difficulty,
                                update_created="2.2"
                                )

            if r.get("level_password", None):
                new_demon.level_password = level_password
                new_demon.save()

            Changelog.objects.create(demon=new_demon,
                                     reason="Added to list",
                                     position=position,
                                     )
            
            functions.order_list_points()
            functions.update_players_list_points_all()
            functions.update_countries_list_points_all()

            return HttpResponseRedirect(reverse_lazy('demonlist:list'))
        
        if r.get("option", None) == "Edit":
            level = r.get("edit_demon", None)
            photo = request.FILES["photo"]
            position = r.get("position", None)
            creator = r.get("creator", None)
            verificator = r.get("verificator", None)
            verification_video = r.get("verification_video", None)
            level_id = r.get("level_id", None)
            object_count = r.get("object_count", None)
            demon_difficulty = r.get("demon_difficulty", None)
            level_password = r.get("level_password", None)

            old_demon = Demon.objects.get(level=level)

            old_position = old_demon.position

            if old_position > int(position):
                Changelog.objects.create(demon=old_demon,
                                reason="Moved",
                                position=int(position),
                                change_number=old_position - int(position),
                                change_type="Up"
                                )
            elif old_position < int(position):
                Changelog.objects.create(demon=old_demon,
                                reason="Moved",
                                position=int(position),
                                change_number=int(position) - old_position,
                                change_type="Down"
                                )
            
            if old_position > int(position):
                demons = Demon.objects.filter(position__lt=old_position, position__gte=int(position))
                for demon in demons:
                    Changelog.objects.create(demon=demon,
                                reason=f"{old_demon.level} was moved up past this demon",
                                position=demon.position + 1,
                                change_number=1,
                                change_type="Down"
                                )
                    demon.position += 1
                    demon.save()
            elif old_position < int(position):
                demons = Demon.objects.filter(position__lte=position, position__gt=old_position)
                for demon in demons:
                    Changelog.objects.create(demon=demon,
                                reason=f"{old_demon.level} was moved down past this demon",
                                position=demon.position - 1,
                                change_number=1,
                                change_type="Up"
                                )
                    demon.position -= 1
                    demon.save()

            if verification_video[:16] == "https://youtu.be":
                verification_video_embed = 'https://www.youtube.com/embed/' + verification_video.split('/')[3]
            elif verification_video[:29] == "https://www.youtube.com/watch":
                verification_video_embed = 'https://www.youtube.com/embed/' + verification_video.split('=')[1]
            else:
                verification_video_embed = None
        
            old_demon.photo=photo
            old_demon.position=int(position)
            old_demon.creator=creator
            old_demon.verificator=verificator
            old_demon.verification_video=verification_video
            old_demon.verification_video_embed=verification_video_embed
            old_demon.level_id=level_id
            old_demon.object_count=object_count
            old_demon.demon_difficulty=demon_difficulty
            
            if r.get("level_password", None):
                old_demon.level_password = level_password
            
            old_demon.save()

            functions.order_list_points()
            functions.update_players_list_points_all()
            functions.update_countries_list_points_all()

            return HttpResponseRedirect(reverse_lazy('demonlist:list'))
        