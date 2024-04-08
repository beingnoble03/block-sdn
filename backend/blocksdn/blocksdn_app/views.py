from django.http import JsonResponse
from .ryu_controller.ethers_interaction import *

def controller(request):
    message_hash = authenticator_contract_interactor()
    resp = {
        "message": message_hash
    }
    return JsonResponse(resp)