"""Demon List views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View

# Models
from django.contrib.auth.models import User
from demonlist.models import Demon, Record, Changelog, Roulette

# Utils
import json

class DemonApi(LoginRequiredMixin, View):
    # Vista del dashboard buscar_vehiculos

    def get(self, request):

        level_id = request.GET.get('level_id', None)

        demon = Demon.objects.values("id", "position", "level", "list_points", "level_id", "level_password", "creator").get(level_id=level_id)

        json_context = json.dumps(demon, indent=None, sort_keys=False, default=str)

        return HttpResponse(json_context, content_type='application/json')