from django.http import JsonResponse
from .ryu_controller.ethers_interaction import *

def controller_register(request):
    message_hash = register_device()
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)

def controller_auth1(request):
    message_hash = auth1()
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)

def controller_auth2(request):
    message_hash = auth2()
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)