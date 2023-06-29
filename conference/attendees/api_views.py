from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from django.views.decorators.http import require_http_methods
import json

from .models import Attendee
from events.models import Conference


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.all()
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid Conference ID"},
                status=400,
            )
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )


#UPDATE DOES NOT WORK. NOT SURE HOW TO FIX
@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            safe=False,
            encoder=AttendeeDetailEncoder,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
                print("the conference name:",content["conference"])
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid Conference ID"},
                status=400,
            )

        example = Attendee.objects.filter(id=id).update(**content)
        print("the content:",content)

        attendee = example
        print("the id:", id)
        print("the attendee:", attendee)
        return JsonResponse(
            attendee,
            safe=False,
            encoder=AttendeeDetailEncoder,
        )
