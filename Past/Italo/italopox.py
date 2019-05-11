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

s1_dpid = 0
s2_dpid = 0
s3_dpid = 0

s1_p1 = 0
s1_p2 = 0
s1_p3 = 0

s2_p1 = 0
s2_p2 = 0
s2_p3 = 0

s3_p1 = 0
s3_p2 = 0
s3_p3 = 0

pre_s1_p1 = 0
pre_s1_p2 = 0
pre_s1_p3 = 0

pre_s2_p1 = 0
pre_s2_p2 = 0
pre_s2_p3 = 0

pre_s3_p1 = 0
pre_s3_p2 = 0
pre_s3_p3 = 0

def _handle_portstats_received (event):
    pass

def _handle_ConnectionUp (event):
    global s1_dpid, s2_dpid, s3_dpid
    print "ConnectionUp: ", dpidToStr(event.connection.dpid)

    for m in event.connection.features.ports:
        if m.name == "switch_1-eth1":
            s1_dpid = event.connection.dpid
            print "switch1_dpid=", s1_dpid
        elif m.name == "switch_2-eth1":
            s2_dpid = event.connection.dpid
            print "switch2_dpid=", s2_dpid
        elif m.name == "switch_3-eth1":
            s3_dpid = event.connection.dpid
            print "switch3_dpid=", s3_dpid

"""
client_1 : 10.0.0.1 : port 1 - switch_1
client_2 : 10.0.0.2 : port 1 - switch_2
client_3 : 10.0.0.3 : port 1 - switch_3
server_1 : 10.0.0.4 : port 2 - switch_1
server_2 : 10.0.0.5 : port 2 - switch_2
server_3 : 10.0.0.6 : port 2 - switch_3
"""

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

        # AddFlows switch_1
        """
        client_1 -> client_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_1 -> client_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_2 -> client_1 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        client_3 -> client_1 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        client_3 -> client_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        server_1 -> server_2 OK
        """
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
        server_1 -> server_3 OK
        """
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
        server_2 -> server_1 OK
        """
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
        server_3 -> server_1 OK
        """
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
        server_3 -> server_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

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

        # AddFlows switch_2
        """
        client_1 -> client_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        client_1 -> client_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_2 -> client_1 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_2 -> client_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_3 -> client_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        server_1 -> server_2 OK
        """
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
        server_1 -> server_3 OK
        """
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
        server_2 -> server_1 OK
        """
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
        server_2 -> server_3 OK
        """
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
        server_3 -> server_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

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

        # AddFlows switch_3
        """
        client_1 -> client_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        client_2 -> client_1 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_2 -> client_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        """
        client_3 -> client_1 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        client_3 -> client_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        """
        server_1 -> server_3 OK
        """
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
        server_2 -> server_1 OK
        """
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
        server_2 -> server_3 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        """
        server_3 -> server_1 OK
        """
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
        server_3 -> server_2 OK
        """
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

def launch ():
    core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)