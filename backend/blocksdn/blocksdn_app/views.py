from django.http import JsonResponse


def controller(request):
    resp = {
        "message": "this is a controller rest-api dumbass"
    }
    return JsonResponse(resp)