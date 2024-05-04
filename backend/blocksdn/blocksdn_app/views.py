from django.http import JsonResponse
from .ryu_controller.ethers_interaction import *
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def controller_register(request):
    data = json.loads(request.body.decode('utf-8'))
    message_hash = register_device(data)
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)

@csrf_exempt
def controller_auth(request):
    data = json.loads(request.body.decode('utf-8'))
    message_hash = auth(data)
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)
