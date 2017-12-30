"""
mn.py:
    Script for running our sample topology on mininet
    and connect it into contorller on remote host.
Usage (example uses IP = 192.168.1.2):
    From the command line:
        sudo python mn.py --ip 192.168.1.2
"""
import argparse
from functools import partial

from mininet.net import Mininet
from mininet.net import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.topo import Topo
from mininet.link import TCLink

class SampleTopology(Topo):
    """
    Subclass of mininet Topo class for
    creating fat-3 topology. 
    """
    def build(self, *args, **params):
        core1 = self.addSwitch(name='core1',dpid="0000000000000201")
        core2 = self.addSwitch(name='core2',dpid="0000000000000202")
        agg1 = self.addSwitch(name='agg1',dpid="0000000000000203")
        agg2 = self.addSwitch(name='agg2',dpid="0000000000000204")
        edge1 = self.addSwitch(name='edge1',dpid="0000000000000205")
        edge2 = self.addSwitch(name='edge2',dpid="0000000000000206")
        edge3 = self.addSwitch(name='edge3',dpid="0000000000000207")
        edge4 = self.addSwitch(name='edge4',dpid="0000000000000208")

        host1 = self.addHost(name='h1')
       	host2 = self.addHost(name='h2')
        host3 = self.addHost(name='h3')
        host4 = self.addHost(name='h4')
        host5 = self.addHost(name='h5')
        host6 = self.addHost(name='h6')
        host7 = self.addHost(name='h7')
        host8 = self.addHost(name='h8')

        self.addLink(host1, edge1)
        self.addLink(host2, edge1)
        self.addLink(host3, edge2)
        self.addLink(host4, edge2)
        self.addLink(host5, edge3)
        self.addLink(host6, edge3)
        self.addLink(host7, edge4)
        self.addLink(host8, edge4)
        self.addLink(agg1, edge1)
        self.addLink(agg1, edge2)
        self.addLink(agg2, edge3)
        self.addLink(agg2, edge4)
        self.addLink(agg1, core1)
        self.addLink(agg2, core1)
        self.addLink(agg1, core2)
        self.addLink(agg2, core2)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('ips', metavar='ip',
                        help='POX Network Controllers IP Addresses',
                        default=['127.0.0.1'], type=str, nargs='*')
    CLI_ARGS = PARSER.parse_args()

    setLogLevel('info')

    RCS = []
    for ip in CLI_ARGS.ips:
        RCS.append(RemoteController('POX-%s' % ip, ip=ip, port=6633))
    NET = Mininet(topo=SampleTopology(), build=False)
    for rc in RCS:
        NET.addController(rc)
    NET.build()
    NET.start()
    CLI(NET)
    NET.stop()
