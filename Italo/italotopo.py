#!/usr/bin/python
 
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
import os
from time import sleep

class MyTopo(Topo):
    "My Topology"
    def __init__(self):
        Topo.__init__(self)

        switch_1 = self.addSwitch('switch_1')
        switch_2 = self.addSwitch('switch_2')
        switch_3 = self.addSwitch('switch_3')

        client_1 = self.addHost('client_1')
        server_1 = self.addHost('server_1')

        client_2 = self.addHost('client_2')
        server_2 = self.addHost('server_2')
        
        client_3 = self.addHost('client_3')
        server_3 = self.addHost('server_3')
         
        self.addLink(switch_1, client_1, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(switch_2, client_2, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 
        self.addLink(switch_3, client_3, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)
        
        self.addLink(switch_1, server_1, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 
        self.addLink(switch_2, server_2, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 
        self.addLink(switch_3, server_3, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 
        
        self.addLink(switch_1, switch_2, port1=3, port2=4, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 
        self.addLink(switch_2, switch_3, port1=3, port2=4, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)  
        self.addLink(switch_3, switch_1, port1=3, port2=4, bw=0.03, delay='10ms', loss=0, max_queue_size=1000, use_htb=True) 

def configureNetwork():
    "Create network"
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    
    client_1 = net.get('client_1')
    print "Client 1", client_1.IP()
    server_1 = net.get('server_1')
    print "Server 1", server_1.IP()
    client_2 = net.get('client_2')
    print "Client 2", client_2.IP()
    server_2 = net.get('server_2')
    print "Server 2", server_2.IP()
    client_3 = net.get('client_3')
    print "Client 3", client_3.IP()
    server_3 = net.get('server_3')
    print "Server 3", server_3.IP()

    client_1.setMAC("0:0:0:0:0:1")
    client_2.setMAC("0:0:0:0:0:2")
    client_3.setMAC("0:0:0:0:0:3")
    server_1.setMAC("0:0:0:0:0:4")
    server_2.setMAC("0:0:0:0:0:5")
    server_3.setMAC("0:0:0:0:0:6")

    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    configureNetwork()