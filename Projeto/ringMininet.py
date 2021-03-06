#!/usr/bin/python
# sudo -E python <nameofthefile> - run
# sudo mn -c - kill
# hx ping hy - test
# pingall - test 2

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.node import Controller
from mininet.cli import CLI
from functools import partial
from mininet.node import RemoteController
from mininet.node import OVSController
from mininet.node import OVSKernelSwitch, Host
import os
from time import sleep

class MyTopo(Topo):
    "Single switch connected to n hosts."

    def __init__(self):
        Topo.__init__(self)
        #Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        #Client-Host
        client1 = self.addHost('client1', ip='10.0.0.1/24')
        client2 = self.addHost('client2', ip='10.0.0.3/24')
        client3 = self.addHost('client3', ip='10.0.0.5/24')

        #Server-Host
        server1 = self.addHost('server1', cls=Host, defaultRoute=None, ip='10.0.0.2/24')
        server2 = self.addHost('server2', cls=Host, defaultRoute=None, ip='10.0.0.4/24')
        server3 = self.addHost('server3', cls=Host, defaultRoute=None, ip='10.0.0.6/24')

        #Links between switches
        self.addLink(s1, s2, bw=0.03, delay='0ms', loss=0, max_queue_size=1000)
        self.addLink(s1, s3, bw=0.03, delay='0ms', loss=0, max_queue_size=1000)
        self.addLink(s2, s3, bw=0.03, delay='0ms', loss=0, max_queue_size=1000)

        #Links between switches and clients
        self.addLink(client1, s1,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)
        self.addLink(client2, s2,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)
        self.addLink(client3, s3,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)

        #Links between switches and servers
        self.addLink(server1, s1,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)
        self.addLink(server2, s2,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)
        self.addLink(server3, s3,  bw=0.03, delay='0ms',
                     loss=0, max_queue_size=1000)


def configureNetwork():
    "Create network and run simple performance test"
    topo = MyTopo()
    #Tenho que apontar o IP para a instancia do ONOS.

    net = Mininet(topo=topo,link=TCLink)

    controlador = net.addController(name='controlador',
    controller=RemoteController,
    ip='127.17.0.5',
    port=8181)
    
    net.start()
    # net.build()

    print ("Dumping host connections")
    dumpNodeConnections(net.hosts)
    

    client1 = net.get('client1')
    client2 = net.get('client2')
    client3 = net.get('client3')
    server1 = net.get('server1')
    server2 = net.get('server2')
    server3 = net.get('server3')

    client1.setMAC("0:0:0:0:0:1")
    client2.setMAC("0:0:0:0:0:3")
    client3.setMAC("0:0:0:0:0:5")
    server1.setMAC("0:0:0:0:0:2")
    server2.setMAC("0:0:0:0:0:4")
    server3.setMAC("0:0:0:0:0:6")   

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    configureNetwork()
