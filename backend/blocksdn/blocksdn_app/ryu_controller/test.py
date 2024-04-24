from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

from web3 import Web3
from flask import Flask, jsonify

class BlockchainController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(BlockchainController, self).__init__(*args, **kwargs)
        self.web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Connect to Ethereum node
        self.app = Flask(__name__)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Add flow entry to forward packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                           ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @app.route('/get_balance', methods=['GET'])
    def get_balance(self):
        # Example function to query balance from blockchain
        balance = self.web3.eth.get_balance('0x1234567890123456789012345678901234567890')
        return jsonify({'balance': balance})

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)  # Run Flask app

    def start(self):
        super(BlockchainController, self).start()
        self.run()

app_manager.require_app('ryu.controller.main')
