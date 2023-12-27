"""Demon List views."""

# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.files.images import ImageFile
from django.db.models import F, Window, Sum
from django.db.models.functions import DenseRank
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

class ModeradorMixin(UserPassesTestMixin):
    def test_func(self):

        print(self.request.user.groups.get())
        if str(self.request.user.groups.get()) == "Mod":
            is_mod = True
        else:
            is_mod = False
        return self.request.user.is_authenticated and is_mod


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
        print(option)

        if option == "best_time":
            records = Record.objects.filter(demon=demon, accepted=True).order_by("best_time")

            records = list(records.values("player__user__username", "player__country__picture", "video", "best_time"))

            print(records)

            return JsonResponse(records, safe=False)
        elif option == "order":
            records = Record.objects.filter(demon=demon, accepted=True)

            records = list(records.values("player__user__username", "player__country__picture", "video", "best_time"))
            print(records)

            return JsonResponse(records, safe=False)


class SubmitRecordView(LoginRequiredMixin, TemplateView):
    """Submit a new record."""

    template_name = 'demonlist/submit_record.html'
    success_url = reverse_lazy('demonlist:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        demons = Demon.objects.all()


        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
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
        players = Profile.objects.filter(list_points__gte=1).annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))
        countries = Country.objects.all().order_by("country")

        context["countries"] = countries
        context["players"] = players
        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("player", None) or r.get("player", None) == "":

            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
            )

            players_filtered = players_annotated.filter(user__username__icontains=r.get("player", None))

            original_positions = {player.id: player.position for player in players_annotated}

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])

            result_list = [
                {
                    'id': player.id,
                    'user__id': player.user.id,
                    'user__username': player.user.username,
                    'list_points': player.list_points,
                    'position': original_positions[player.id],
                    'country__picture': player.country.picture.url,
                }
                for player in players_final
            ]

            return JsonResponse(result_list, safe=False)
        
        if r.get("country", None) or r.get("country", None) == "":
            
            countries_annotated = Country.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
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

            return JsonResponse(result_list, safe=False)
        
        if r.get("option", None):
            
            if r.get("option", None) == "Nations":

                countries = Country.objects.filter(list_points__gte=1).annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))

                countries = list(countries.values("id", "picture", "list_points", "position", "country"))

                return JsonResponse(countries, safe=False)
            
            elif r.get("option", None) == "Individual":
                players = Profile.objects.filter(list_points__gte=1).annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))

                players = list(players.values("id", "user__id", "user__username", "list_points", "position", "country__picture"))

                return JsonResponse(players, safe=False)

        if r.get("select_country", None) or r.get("select_country", None) == "":
            
            players_annotated = Profile.objects.filter(list_points__gte=1).annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
            )

            if r.get("select_country", None):
                players_filtered = players_annotated.filter(country__country=r.get("select_country", None))
            else:
                players_filtered = players_annotated

            original_positions = {player.id: player.position for player in players_annotated}

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])

            result_list = [
                {
                    'id': player.id,
                    'user__id': player.user.id,
                    'user__username': player.user.username,
                    'list_points': player.list_points,
                    'position': original_positions[player.id],
                    'country__picture': player.country.picture.url,
                }
                for player in players_final
            ]

            print(players_annotated)
            print(players_filtered)
            print(original_positions)
            print(result_list)

            return JsonResponse(result_list, safe=False)

class CheckRecordsView(LoginRequiredMixin, ModeradorMixin, TemplateView):
    # Return check records view
    template_name = "demonlist/check_records.html"
    success_url = reverse_lazy('demonlist:check_records')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

            records = list(records.values("id", "player__user__username", "demon__level", "video", "raw_footage", "mod_notes"))
            return JsonResponse(records, safe=False)
        
        if r.get("accept_id", None):
            record = Record.objects.get(id=r.get("accept_id", None))
            mod_notes = r.get("mod_notes", None)

            record.accepted = True
            record.mod_notes = mod_notes
            record.mod = self.request.user.profile
            record.save()

            player = record.player
            player.list_points += record.demon.list_points
            player.save()

            functions.update_countries_list_points()

            return JsonResponse(record.id, safe=False)
        
        if r.get("cancel_id", None):
            record = Record.objects.get(id=r.get("cancel_id", None))
            mod_notes = r.get("mod_notes", None)

            if record.accepted:
                player = record.player
                player.list_points -= record.demon.list_points
                player.save()

                functions.update_countries_list_points()

            record.accepted = False
            record.mod_notes = mod_notes
            record.mod = self.request.user.profile
            record.save()

            return JsonResponse(record.id, safe=False)
        
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

            new_demon = Demon.objects.create(level=level,
                                photo=photo,
                                position=position,
                                creator=creator,
                                verificator=verificator,
                                verification_video=verification_video,
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

            if old_position > position:
                Changelog.objects.create(demon=old_demon,
                                reason="Moved",
                                position=position,
                                change_number=old_position - position,
                                change_type="Up"
                                )
            elif old_position < position:
                Changelog.objects.create(demon=old_demon,
                                reason="Moved",
                                position=position,
                                change_number=position - old_position,
                                change_type="Down"
                                )
            
            if old_position > position:
                demons = Demon.objects.filter(position__lte=old_position, position__gte=position)
                for demon in demons:
                    Changelog.objects.create(demon=demon,
                                reason=f"{old_demon.level} was moved up past this demon",
                                position=demon.position + 1,
                                change_number=1,
                                change_type="Down"
                                )
                    demon.position += 1
                    demon.save()
            elif old_position < position:
                demons = Demon.objects.filter(position__lte=position, position__gte=old_position)
                for demon in demons:
                    Changelog.objects.create(demon=demon,
                                reason=f"{old_demon.level} was moved down past this demon",
                                position=demon.position - 1,
                                change_number=1,
                                change_type="Up"
                                )
                    demon.position -= 1
                    demon.save()
        
            old_demon.photo=photo
            old_demon.position=position
            old_demon.creator=creator
            old_demon.verificator=verificator
            old_demon.verification_video=verification_video
            old_demon.level_id=level_id
            old_demon.object_count=object_count
            old_demon.demon_difficulty=demon_difficulty
            
            if r.get("level_password", None):
                old_demon.level_password = level_password
            
            old_demon.save()

            functions.order_list_points()
            functions.update_players_list_points()
            functions.update_countries_list_points()

            return HttpResponseRedirect(reverse_lazy('demonlist:list'))
        