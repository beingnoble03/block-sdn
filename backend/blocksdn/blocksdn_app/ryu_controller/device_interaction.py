from .constants import DEVICE_TYPE_MAP, RYU_CONTROLLER_WSGI_URL
import requests

# TODO: IoT device type implementation is a part of BTP extension
def get_device_type(device_id) -> int:
    """
    Gets the device type, returns 0 as device type if the
    device's mac is not found in map
    """
    t = DEVICE_TYPE_MAP.get(device_id)
    
    if t == None:
        return 0
    
    return t

def is_device_valid(device_id) -> bool:
    """
    Checks if the device is valid
    """
    return DEVICE_TYPE_MAP.get(device_id) != None

def inform_device(device_id) -> None:
    """
    Informs the device about the authentication
    """
    requests.post(RYU_CONTROLLER_WSGI_URL, json={"device_id": device_id})