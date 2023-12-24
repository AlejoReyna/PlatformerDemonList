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
    
class GuidelinesView(TemplateView):
    """Return guidelines view."""

    template_name = 'guidelines.html'