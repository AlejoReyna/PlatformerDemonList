"""Demon List views."""

# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.images import ImageFile
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, TemplateView

# Models
from demonlist.models import Demon, Record
from users.models import Profile

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
        records = Record.objects.filter(demon=demon)
        records_complete = records.filter(percentage=100)

        context["records"] = records
        context["records_complete"] = records_complete

        return context

class SubmitRecordView(LoginRequiredMixin, TemplateView):
    """Submit a new record."""

    template_name = 'demonlist/submit_record.html'
    success_url = reverse_lazy('posts:list')

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
        percentage = r.get("percentage", None)
        video = r.get("video", None)
        raw_footage = r.get("raw_footage", None)
        notes = r.get("notes", None)

        print(r)

        Record.objects.create(demon=Demon.objects.get(level=demon),
                            player=Profile.objects.get(id=profile),
                            percentage=percentage,
                            video=video,
                            raw_footage=raw_footage,
                            notes=notes,
                            )
        
        return HttpResponseRedirect(reverse_lazy('demonlist:list'))


