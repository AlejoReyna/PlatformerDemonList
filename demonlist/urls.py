"""DemonList URLs."""

# Django
from django.urls import path

# Views
from demonlist import views

urlpatterns = [

    path(
        route='',
        view=views.DemonListView.as_view(),
        name='list'
    ),
    path(
        route='demons/<int:pk>/',
        view=views.DemonDetailView.as_view(),
        name='detail'
    ),
    path(
        route='submit_record/',
        view=views.SubmitRecordView.as_view(),
        name='submit_record'
    ),

]
