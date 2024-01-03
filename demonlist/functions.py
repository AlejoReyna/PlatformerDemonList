# Django
from django.db.models import Sum, Q, F

# Models
from django.contrib.auth.models import User
from users.models import Profile, Country
from demonlist.models import Demon, Record, values_list_points



def order_list_points():
    demons = Demon.objects.all()
    for demon in demons:
        demon.list_points = values_list_points[demon.position - 1]
        demon.save()

def update_players_list_points(player):
    list_points = 0
    demons = Record.objects.filter(player=player, accepted=True).values("demon__list_points")
    for demon in demons:
        list_points += demon["demon__list_points"]
    player.list_points = list_points
    player.save()

def update_countries_list_points(country):
    demons = Record.objects.filter(player__country=country, accepted=True).values("demon").distinct().values("demon__list_points")

    list_points = 0
    for demon in demons:
        list_points += demon["demon__list_points"]

    country.list_points = list_points
    country.save()

def update_players_list_points_all():
    players = Profile.objects.annotate(total_list_points=Sum('record__demon__list_points', filter=Q(record__accepted=True))).distinct()

    for player in players:
        player.list_points = player.total_list_points or 0
        player.save()

def update_countries_list_points_all():
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

def update_top_order(demon):
    records = Record.objects.filter(demon=demon, accepted=True)
    top_order = 1

    for record in records:
        record.top_order = top_order
        record.save()
        top_order += 1


def update_top_all():
    demons = Demon.objects.all()
    for demon in demons:
        records = Record.objects.filter(demon=demon, accepted=True).order_by("best_time")
        top_best_time = 1

        for record in records:
            record.top_best_time = top_best_time
            record.save()
            top_best_time += 1

        records = Record.objects.filter(demon=demon, accepted=True)
        top_order = 1

        for record in records:
            record.top_order = top_order
            record.save()
            top_order += 1


def upload_bots_albania():
    for i in range(2000, 3000):
        user = User.objects.create(username=f"i-user{i}", password=f"i-password{i}")
        Profile.objects.create(user=user,
                               list_points=3400,
                               country=Country.objects.get(country="Albania")
                               )