from django.http import JsonResponse
<<<<<<< HEAD


def controller(request):
    resp = {
        "message": "this is a controller rest-api dumbass"
=======
from .ryu_controller.ethers_interaction import *

def controller(request):
    message_hash = authenticator_contract_interactor()
    resp = {
        "message": message_hash
>>>>>>> f498f9add8a88ae9bab3f356f9d05cfec0ab88cf
    }
    return JsonResponse(resp)