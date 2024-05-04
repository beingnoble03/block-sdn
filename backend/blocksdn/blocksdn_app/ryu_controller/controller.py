# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, inet, ether
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types, ipv4
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response
import socket
import json
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, icmp

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}
        wsgi = kwargs['wsgi']
        wsgi.register(SimpleSwitchController, {'simple_switch_app': self})
                # Default MAC and IP addresses
        self.controller_mac = '00:00:00:00:00:01'  # MAC address of the controller
        self.controller_ip = '10.0.0.1'  # IP address of the controller
        self.host2_mac = '00:00:00:00:00:02'  # MAC address of host 2
        self.host2_ip = '10.0.0.2'  # IP address of host 2

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.datapaths[datapath.id] = datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s", dpid, dst, in_port)
        # print(pkt)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    # @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    # def packet_in_handler(self, ev):
    #     msg = ev.msg
    #     datapath = msg.datapath
    #     ofproto = datapath.ofproto
    #     parser = datapath.ofproto_parser

    #     pkt = packet.Packet(msg.data)
    #     eth = pkt.get_protocols(ethernet.ethernet)[0]

    #     if eth.ethertype == ether_types.ETH_TYPE_IP:
    #         ip = pkt.get_protocol(ipv4.ipv4)
    #         if ip:
    #             if eth.dst == self.target_host_mac:
    #                 self.logger.info("Received packet destined to target host (%s): %s", self.target_host_mac, ip)
    #                 print("Received packet destined to target host:", ip)

    def send_packet(self, dst_ip, src_ip):        
        # Create a ping packet
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=ether.ETH_TYPE_IP,
                                        dst='ff:ff:ff:ff:ff:ff',
                                        src='00:00:00:00:00:01'))
        pkt.add_protocol(ipv4.ipv4(dst=dst_ip,
                                src=src_ip,
                                proto=socket.IPPROTO_ICMP))

        # Serialize the packet to bytes
        pkt.serialize()

        # Get the datapath object associated with the source IP address
        # datapath = self.mac_to_port[1].get(src_ip)
        datapath = self.datapaths.get(1)

        if datapath is None:
            print(f"No datapath found for source IP {src_ip}")
            return

        # Create an OpenFlow message that instructs the switch to send the packet
        actions = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_FLOOD)]
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=datapath.ofproto.OFP_NO_BUFFER,
            in_port=datapath.ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=pkt.data)

        # Send the OpenFlow message to the switch
        datapath.send_msg(out)

    def send_packet_to_host(self, eth_dst, out_port):
        # Get the datapath
        datapath = self.datapaths.get(1)

        if datapath is None:
            print(f"No datapath found with id = 1")
            return
        
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Create an Ethernet frame
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=ether.ETH_TYPE_IP,
                                        dst=eth_dst))
        
        # Create an output action to send the packet
        actions = [parser.OFPActionOutput(out_port)]

        # Create a flow mod message to install a flow entry in the switch
        out = parser.OFPPacketOut(datapath=datapath,
                                buffer_id=ofproto.OFP_NO_BUFFER,
                                in_port=ofproto.OFPP_CONTROLLER,
                                actions=actions,
                                data=pkt)
        
        # Send the packet out of the specified port
        datapath.send_msg(out)

    def send_ping(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Create ICMP echo request packet
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=ether_types.ETH_TYPE_IP,
                                            dst=self.host2_mac,
                                            src=self.controller_mac))
        pkt.add_protocol(ipv4.ipv4(dst=self.host2_ip,
                                    src=self.controller_ip,
                                    proto=socket.IPPROTO_ICMP))
        pkt.add_protocol(icmp.icmp(type_=icmp.ICMP_ECHO_REQUEST,
                                    code=0,
                                    csum=0,
                                    data=icmp.echo(id_=0, seq=0, data='Login IoT (test)'.encode())))

        # Serialize the packet
        pkt.serialize()

        # Create an OpenFlow message to send the packet
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(datapath=datapath,
                                    buffer_id=ofproto.OFP_NO_BUFFER,
                                    in_port=ofproto.OFPP_CONTROLLER,
                                    actions=actions,
                                    data=pkt.data)
        
        # Send the packet out of the specified port
        datapath.send_msg(out)


class SimpleSwitchController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleSwitchController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data['simple_switch_app']

    @route('simpleswitch', '/simpleswitch/', methods=['POST'])
    def send_packet(self, req, **kwargs):
        data = req.json if req.body else {}
        device_id = data.get('device_id')
        dp = self.simple_switch_app.datapaths.get(1)
        
        self.simple_switch_app.send_ping(dp)
        self.simple_switch_app.logger.info("packet in %s %s %s", "1", device_id, 1)
        
        return Response(content_type='application/json ; charset=UTF-8', body=json.dumps({'status': 'success'}))
