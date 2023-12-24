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
from demonlist.models import Demon, Record
from users.models import Profile, Country

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
    context_object_name = "demon"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        demon = self.get_object()
        records = Record.objects.filter(demon=demon, accepted=True)

        context["records"] = records

        return context

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
        profile = r.get("profile", None)
        video = r.get("video", None)
        raw_footage = r.get("raw_footage", None)
        notes = r.get("notes", None)

        print(r)

        Record.objects.create(demon=Demon.objects.get(level=demon),
                            player=Profile.objects.get(id=profile),
                            video=video,
                            raw_footage=raw_footage,
                            notes=notes,
                            )
        
        return HttpResponseRedirect(reverse_lazy('demonlist:list'))

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

            return JsonResponse(record.id, safe=False)
        
        if r.get("cancel_id", None):
            record = Record.objects.get(id=r.get("cancel_id", None))
            mod_notes = r.get("mod_notes", None)

            record.accepted = False
            record.mod_notes = mod_notes
            record.mod = self.request.user.profile
            record.save()

            return JsonResponse(record.id, safe=False)
        
class StatsViewerView(TemplateView):
    # Return stats viewer view
    template_name = "demonlist/stats_viewer.html"
    success_url = reverse_lazy('demonlist:stats_viewer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = Profile.objects.annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))
        
        context["players"] = players

        return context
    
    def post(self, request):
        r = request.POST
        
        print(r)

        if r.get("player", None) or r.get("player", None) == "":
            
            players_annotated = Profile.objects.annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
            )

            players_filtered = players_annotated.filter(user__username__icontains=r.get("player", None))

            original_positions = {player.id: player.position for player in players_annotated}

            players_final = sorted(players_filtered, key=lambda player: original_positions[player.id])

            result_list = [
                {
                    'id': player.id,
                    'user__username': player.user.username,
                    'list_points': player.list_points,
                    'position': original_positions[player.id],
                    'country': player.country,
                }
                for player in players_final
            ]

            return JsonResponse(result_list, safe=False)
        
        if r.get("country", None) or r.get("country", None) == "":
            
            countries_annotated = Country.objects.annotate(
                position=Window(expression=DenseRank(), order_by=F('list_points').desc())
            )

            countries_filtered = countries_annotated.filter(country__icontains=r.get("country", None))

            original_positions = {country.id: country.position for country in countries_annotated}

            countries_final = sorted(countries_filtered, key=lambda country: original_positions[country.id])

            result_list = [
                {
                    'id': country.id,
                    'country': country.country,
                    'position': original_positions[country.id],
                    'list_points': country.list_points,
                }
                for country in countries_final
            ]

            return JsonResponse(result_list, safe=False)
        
        if r.get("option", None):
            
            if r.get("option", None) == "Nations":

                countries = Country.objects.annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))
                print(countries)

                countries = list(countries.values("id", "country", "list_points", "position"))

                return JsonResponse(countries, safe=False)
            
            elif r.get("option", None) == "Individual":
                players = Profile.objects.annotate(position=Window(expression=DenseRank(), order_by=F('list_points').desc()))

                players = list(players.values("id", "user__username", "list_points", "position", "country"))

                return JsonResponse(players, safe=False)
