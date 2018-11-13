#!/usr/bin/python

#Created by Arnaldo, list 2 mininet.
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
        self.addLink(client1,s1, bw=0.03)
        self.addLink(server1,s1, bw=0.03)

        self.addLink(client2,s2, bw=0.03)
        self.addLink(server2,s2, bw=0.03)

        self.addLink(client3,s3, bw=0.03)
        self.addLink(server3,s3, bw=0.03)

        #Switch-Switch Link
        self.addLink(s1,s2, bw=0.03)
        self.addLink(s1,s3, bw=0.03)
        self.addLink(s2,s3, bw=0.03)




def myNetwork():
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost,link=TCLink,
		controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()

	info( '*** Starting network\n')

    print "Dumping host connections"
	dumpNodeConnections(net.hosts)

    #não sei se precisa
	client1=net.get('client1')
	server1=net.get('server1')
	client2=net.get('client2')
	server2=net.get('server2')
    client3=net.get('client3')
	server3=net.get('server3')

    client1.setMAC("0:0:0:0:0:1")
	server1.setMAC("0:0:0:0:0:2")
	client2.setMAC("0:0:0:0:0:3")
	server2.setMAC("0:0:0:0:0:4")
	client3.setMAC("0:0:0:0:0:5")
	server3.setMAC("0:0:0:0:0:6")

	info( '\n' )
	info( "*** Starting iperf Measurement ***\n" )
	info( '\n' )
	info( "*** Stop old iperf server ***" )
	os.system('pkill -f \'iperf -s\'')
	sleep(1)
	info( '\n' )

	CLI(net)
	net.stop()


def simpleTest():
    # Create and test a simple network
    topo = MyTopo()

    net = Mininet(topo=topo, host=CPULimitedHost,link=TCLink,
		controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    #simpleTest()
    myNetwork()
