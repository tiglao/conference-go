from django.http import JsonResponse
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json

from .models import Presentation
from events.models import Conference


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.all()
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
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
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                print("try loop/conference is in content/create conference variable equal to Conference object with id=specific_conference_name:", conference)

                content["conference"] = conference
                print("should be equal to above. specific conference name:", content["conference"])

                #this statement checks if the key "conference" is in the content and makes content["conference"] = name of the conference

        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid Conference ID"},
                status=400,
            )

        print("id in example:", id)
        print("before content:", content)

        example = Presentation.objects.filter(id=id).update(**content)
        print("EXAMPLE::: returns the number of presentations updated:", example)

        print("the id:", id)
        presentation = example
        # presentation = Presentation.objects.create(id=id)
        print("should be the same as the last:", presentation)


        print("JSON:",JsonResponse(
            presentation,
            safe=False,
            encoder=PresentationDetailEncoder,
        ))
        return JsonResponse(
            presentation,
            safe=False,
            encoder=PresentationDetailEncoder,
        )
