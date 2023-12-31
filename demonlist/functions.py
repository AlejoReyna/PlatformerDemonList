from django.db.models import Sum

from users.models import Profile, Country
from demonlist.models import Demon, Record, values_list_points

def order_list_points():
    demons = Demon.objects.all()
    for demon in demons:
        demon.list_points = values_list_points[demon.position - 1]
        demon.save()

def update_players_list_points():
    players = Profile.objects.all()
    for player in players:
        list_points = 0
        demons = Record.objects.filter(player=player, accepted=True).values("demon__list_points")
        for demon in demons:
            list_points += demon["demon__list_points"]
        player.list_points = list_points
        player.save()

def update_countries_list_points():
    countries = Country.objects.all()

    for country in countries:
        demons = Record.objects.filter(player__country=country, accepted=True).values("demon").distinct().values("demon__list_points")

        list_points = 0
        for demon in demons:
            list_points += demon["demon__list_points"]

        country.list_points = list_points
        country.save()

def update_top_best_time(demon):
    records = Record.objects.filter(demon=demon, accepted=True).order_by("best_time")
    top_best_time = 1

    for record in records:
        record.top_best_time = top_best_time
        record.save()
        top_best_time += 1
