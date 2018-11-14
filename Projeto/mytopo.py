#!/usr/bin/python
#sudo -E python mytopo.py create
#sudo mn -c clear


#Created by Arnaldo,  mininet.
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
    def __init__(self):
        Topo.__init__(self)
        #Switches
        s1=self.addSwitch('s1')
        s2=self.addSwitch('s2')
        s3=self.addSwitch('s3')

        #Client and Servers
        client1=self.addHost('client1')
        server1=self.addHost('server1')

        client2=self.addHost('client2')
        server2=self.addHost('server2')

        client3=self.addHost('client3')
        server3=self.addHost('server3')


        #Host-Switch Links
        self.addLink(client1,s1, bw=0.03,delay='1ms', loss=0, max_queue_size=100, use_htb=True)
        self.addLink(server1,s1, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)

        self.addLink(client2,s2, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)
        self.addLink(server2,s2, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)

        self.addLink(client3,s3, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)
        self.addLink(server3,s3, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)

        #Switch-Switch Link
        self.addLink(s1,s2,port1=3,port2=4, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)
        self.addLink(s2,s3,port1=3,port2=4, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)
        self.addLink(s3,s1,port1=3,port2=4, bw=0.03, delay='1ms', loss=0, max_queue_size=100, use_htb=True)




def myNetwork():
	topo = MyTopo()
	net = Mininet(topo=topo, host=CPULimitedHost,link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
	net.start()

	print "Dumping host connections"
	dumpNodeConnections(net.hosts)


	client1=net.get('client1')
	client2=net.get('client2')
	client3=net.get('client3')
	server2=net.get('server2')
	server1=net.get('server1')
	server3=net.get('server3')

	print "Client 1 - ", client1.IP()
	print "Client 2 - ", client2.IP()
	print "Client 3 - ", client3.IP()
	print "Server 1 - ", server1.IP()
	print "Server 2 - ", server2.IP()
	print "Server 3 - ", server3.IP()

	client1.setMAC("0:0:0:0:0:1")
	client2.setMAC("0:0:0:0:0:2")
	client3.setMAC("0:0:0:0:0:3")
	server1.setMAC("0:0:0:0:0:4")
	server2.setMAC("0:0:0:0:0:5")
	server3.setMAC("0:0:0:0:0:6")

	CLI(net)
	net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
