#!/usr/bin/env python

"""
"""
from mininet.topo import Topo

class Tower( Topo ):
    "Internet Topology Zoo Specimen."

    def addSwitch( self, name, **opts ):
        kwargs = { 'protocols' : 'OpenFlow13' }
        kwargs.update( opts )
        return super(Tower, self).addSwitch( name, **kwargs )

    def __init__( self ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self )

	#Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

	#Client-Host
	client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        client3 = self.addHost('client3')

	#Server-Host
	server1 = self.addHost('server1')
        server2 = self.addHost('server2')
        server3 = self.addHost('server3')

	#Links between switches
        self.addLink(s1, s2, bw=0.03)
        self.addLink(s1, s3, bw=0.03)
        self.addLink(s2, s3, bw=0.03)

        #Links between switches and clients
        self.addLink(client1, s1, bw=0.03)
        self.addLink(client2, s2, bw=0.03)
        self.addLink(client3, s3, bw=0.03)

        #Links between switches and servers
        self.addLink(server1, s1, bw=0.03)
        self.addLink(server2, s2, bw=0.03)
        self.addLink(server3, s3, bw=0.03)

topos = { 'tower': ( lambda: Tower() ) }

if __name__ == '__main__':
    from onosnet import run
    run( Tower() )


        

