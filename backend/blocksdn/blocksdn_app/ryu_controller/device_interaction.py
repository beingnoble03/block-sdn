from .constants import DEVICE_TYPE_MAP

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