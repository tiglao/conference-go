from django.http import JsonResponse
from .models import Conference, Location, State
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json

from .acls import grab_image, grab_coordinates, grab_weather

class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = ["name"]


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "state",
        "weather",
    ]

    def default(self,o):
        if hasattr(o, 'as_dict'):
            return o.as_dict()
        return super().default(o)


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
        # "state",
        "image_url",
    ]


@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
        )
    else:
        content = json.loads(request.body)
        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_conference(request, id):
    if request.method == "GET":
        conference = Conference.objects.get(id=id)
        lat = grab_coordinates(Location.city, Location.state)
        lon = grab_coordinates(Location.city, Location.state)
        conference.weather = grab_weather(lat, lon)
        # print(conference.weather)
    #     conference.update(weather)
        return JsonResponse(
            conference,
            safe=False,
            encoder=ConferenceDetailEncoder,
        )
    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=id)


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations},
            encoder=LocationListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        photo = grab_image(content["city"], content["state"])
        content.update(photo)
        location = Location.objects.create(**content)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_location(request, id):
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            safe=False,
            encoder=LocationDetailEncoder,
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)

        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
