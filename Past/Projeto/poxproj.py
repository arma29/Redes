# ext/poxl2.py
# cd pox/
# python pox.py --verbose poxproj py log --no-default --file=/tmp/mylog.log

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.packet_base import packet_base
from pox.lib.packet.packet_utils import *
import pox.lib.packet as pkt
from pox.lib.recoco import Timer
import time

#mininet> net
#client1 client1-eth0:s1-eth1
#client2 client2-eth0:s2-eth1
#client3 client3-eth0:s3-eth1
#server1 server1-eth0:s1-eth2
#server2 server2-eth0:s2-eth2
#server3 server3-eth0:s3-eth2
#s1 lo:  s1-eth1:client1-eth0 s1-eth2:server1-eth0 s1-eth3:s2-eth3 s1-eth4:s3-eth3
#s2 lo:  s2-eth1:client2-eth0 s2-eth2:server2-eth0 s2-eth3:s1-eth3 s2-eth4:s3-eth4
#s3 lo:  s3-eth1:client3-eth0 s3-eth2:server3-eth0 s3-eth3:s1-eth4 s3-eth4:s2-eth4
#c0

#Rules
    # Servidor n 1 para servidor n 2
    # Servidor n 2 para o servidor n 3
    # Servidor n 3 para o servidor n
    #
    # Cliente n 1, n 2 do cliente, n 3 do cliente
    # podem se comunicar entre si

# Switch 1, Switch 2 e Switch 3
# podem se comunicar com o controlador de dominio
# (ao contrario de todos os outros componentes,
# o controlador de dominio eh executado diretamente na VM do ONUS
# e nao num host virtual separado).

#3 Switches
s1_dpid=0
s2_dpid=0
s3_dpid=0


#S1 tem 4 Links
s1_p1=0
s1_p2=0
s1_p3=0


#S2 tem 4 links
s2_p1=0
s2_p2=0
s2_p3=0


#S3 tem 4 links
s3_p1=0
s3_p2=0
s3_p3=0


########### pt2 pre
#S1 tem 4 Links
pre_s1_p1=0
pre_s1_p2=0
pre_s1_p3=0


#S2 tem 4 links
pre_s2_p1=0
pre_s2_p2=0
pre_s2_p3=0


#S3 tem 4 links
pre_s3_p1=0
pre_s3_p2=0
pre_s3_p3=0

###############
def _handle_portstats_received(event):
    pass

################
def _handle_ConnectionUp (event):
    global s1_dpid, s2_dpid, s3_dpid
    print "ConnectionUp: ",dpidToStr(event.connection.dpid)

    for m in event.connection.features.ports:
         if m.name == "s1-eth1":
           s1_dpid = event.connection.dpid
           print "s1_dpid=", s1_dpid
         elif m.name == "s2-eth1":
           s2_dpid = event.connection.dpid
           print "s2_dpid=", s2_dpid
         elif m.name == "s3-eth1":
           s3_dpid = event.connection.dpid
           print "s3_dpid=", s3_dpid

##################
# client1 - 10:01
# client2 - 10:02
# client3 - 10:03
# server1 - 10:04
# server2 - 10:05
# server3 - 10:06

def _handle_PacketIn(event):
    global s1_dpid, s2_dpid, s3_dpid
    packet = event.parsed
    print "_handle_PacketIn is called, packet.type:", packet.type, " event.connection.dpid:", event.connection.dpid

    # Switch 1
    if event.connection.dpid == s1_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)

        # AddFlows s1
        #Client - Client

        #client1 - client2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client1 - client3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client2 - client1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)


        #client3 - client1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)


        #client3 - client2 Intermediare
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        #Server - Server

        #server1 - server2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        #server1 - server3 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)
        """

        """
        #server2 - server1 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)
        """

        #server3 - server1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        """
        #server3 - server2 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)
        """

    # Switch 2
    if event.connection.dpid == s2_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)

        # AddFlows s2
        #Client - Client

        #client1 - client2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)


        #client2 - client1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client2 - client3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client3 - client2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)


        #client1 - client3 Intermediare
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #Server - Server

        #server1 - server2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        """
        #server1 - server3 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)
        """

        """
        #server2 - server1 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)
        """

        #server2 - server3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        #server3 - server2 Test
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)
        """

    # Switch 3
    if event.connection.dpid == s3_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        # AddFlows s3
        #Client - Client

        #client1 - client3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)



        #client2 - client3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)


        #client3 - client1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client3 - client2 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)


        #client2 - client1 Intermediare
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        #Server - Server

        """
        #server1 - server3 Teste
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)
        """

        """
        #server2 - server1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)
        """

        #server2 - server3 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)


        #server3 - server1 Basic
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        #server3 - server2 Teste
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg
        """

def launch ():
    core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
