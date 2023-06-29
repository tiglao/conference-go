from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .models import Conference, Location, State
from common.json import ModelEncoder


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
    ]

    def get_extra_data(self, o):
        return { "state": o.state.abbreviation }


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = ["name"]


class ConferenceDetailEncoder(ModelEncoder):
    """
    add model type to use common json file
    """
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
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }

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
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location ID"},
                status=400,
            )
        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_conference(request, id):
    if request.method == "GET":
        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference,
            safe=False,
            encoder=ConferenceDetailEncoder,
        )
    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "location" in content:
                location = Location.objects.get(id=content["location"])
                content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location ID"},
                status=400,
            )

        Conference.objects.filter(id=id).update(**content)

        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference,
            safe=False,
            encoder=ConferenceDetailEncoder,
        )

        # content = json.loads(request.body)
        # try:
        #     if "location" in content:
        #         location = Location.objects.get(id=content["location"])
        #         content["location"] = location
        # except Location.DoesNotExist:
        #     return JsonResponse(
        #         {"message": "Invalid location ID"},
        #         status=400,
        #     )

        # Conference.objects.filter(id=id).update(**content)
        # print(content)
        # conference = Conference.objects.create(id=id)
        # print("what is this", conference)
        # return JsonResponse(
        #     conference,
        #     encoder=ConferenceDetailEncoder,
        #     safe=False,
        # )


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method=="GET":
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
        location = Location.objects.create(**content)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
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
