"""DemonList URLs."""

# Django
from django.urls import path

# Views
from demonlist.views import views, views_api

urlpatterns = [

    path(
        route='',
        view=views.DemonListView.as_view(),
        name='list'
    ),
    path(
        route='demons/<int:position>/',
        view=views.DemonDetailView.as_view(),
        name='detail'
    ),
    path(
        route='submit_record/',
        view=views.SubmitRecordView.as_view(),
        name='submit_record'
    ),
    path(
        route='stats_viewer/',
        view=views.StatsViewerView.as_view(),
        name='stats_viewer'
    ),
    path(
        route='check_records/',
        view=views.CheckRecordsView.as_view(),
        name='check_records'
    ),
    path(
        route='check_verifications/',
        view=views.CheckVerificationsView.as_view(),
        name='check_verifications'
    ),
    path(
        route='add_edit_demon/',
        view=views.AddEditDemonView.as_view(),
        name='add_edit_demon'
    ),
    path(
        route='roulette/<int:pk>',
        view=views.RouletteView.as_view(),
        name='roulette'
    ),
    path(
        route='select_roulette/',
        view=views.SelectRouletteView.as_view(),
        name='select_roulette'
    ),

    # API

    path(
        route='api/demon/',
        view=views_api.DemonApi.as_view(),
        name='demon_api'
    ),
]
