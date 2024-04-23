from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
allowed_ips = {}

class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    def packet_handler(self, datapath, port, pkt):
        # Get the IP address from the packet
        ip = pkt.get_protocol(ipv4.ipv4)
        if ip:
            src_ip = ip.src
            dst_ip = ip.dst
            if src_ip not in allowed_ips:
                # Drop the packet
                return
            if dst_ip not in allowed_ips:
                # Drop the packet
                return
        
        # Continue with the rest of the packet handling code
