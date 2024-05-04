from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController

class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Add hosts
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Host4 = self.addHost('h4')
        
        # Add switch
        Switch1 = self.addSwitch('s1')

        # Add links
        self.addLink(Host1,Switch1)
        self.addLink(Host2,Switch1)
        self.addLink(Host3,Switch1)
        self.addLink(Host4,Switch1)


def MyMininet():
    net = Mininet(controller=RemoteController)

    # Add hosts
    Host1 = net.addHost('h1')
    Host2 = net.addHost('h2')
    Host3 = net.addHost('h3')
    Host4 = net.addHost('h4')
    
    # Add switch
    Switch1 = net.addSwitch('s1')

    # Add links
    net.addLink(Host1,Switch1)
    net.addLink(Host2,Switch1)
    net.addLink(Host3,Switch1)
    net.addLink(Host4,Switch1)

    net.start()
    return net

topos = {'mytopo' : (lambda: MyTopo())}
