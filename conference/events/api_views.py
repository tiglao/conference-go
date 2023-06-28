from django.http import JsonResponse

from .models import Conference, Location

from common.json import ModelEncoder
# from json import JSONEncoder


#move this to json in common
# class ModelEncoder(JSONEncoder):
#     """
#     Create modelencoder for definition default
#     """
#     def default(self, o):
#         d = {}
#         for property in self.properties:
#             value = getattr(o, property)
#             d[property] = value
#         return d

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


def api_list_locations(request):
    """
    Lists the location names and the link to the location.

    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.

    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """

    # response = []
    locations = Location.objects.all()
    return JsonResponse(
        {"locations": locations},
        encoder=LocationListEncoder,
    )
    # for location in locations:
    #     response.append(
    #         {
    #             "name": location.name,
    #             "href": location.get_api_url(),
    #         }
    # #     )
    # return JsonResponse({"locations": response})


    # locations = [
    #     {
    #         "name": location.name,
    #         "href": location.get_api_url(),
    #     }
    #     for location in Location.objects.all()
    # ]
    # return JsonResponse({"locations": locations})

def api_show_location(request, id):
    """
    Returns the details for the Location model specified
    by the id parameter.

    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.

    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "state": the two-letter abbreviation for the state,
    }
    """
    location = Location.objects.get(id=id)
    return JsonResponse(
        # {
        #     "name": location.name,
        #     "city": location.city,
        #     "room_count": location.room_count,
        #     "created": location.created,
        #     "updated": location.updated,
        #     "state": location.state.abbreviation,
        # }
        location,
        safe=False,
        encoder=LocationDetailEncoder,
    )
