# ext/starPox.py

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

'''
mininet> net
h1 h1-eth0:s2-eth2
h2 h2-eth0:s2-eth3
h3 h3-eth0:s3-eth2
h4 h4-eth0:s3-eth3
h5 h5-eth0:s4-eth2
h6 h6-eth0:s4-eth3
h7 h7-eth0:s5-eth2
h8 h8-eth0:s5-eth3
h9 h9-eth0:s5-eth4
h10 h10-eth0:s1-eth5
s1 lo:  s1-eth1:s2-eth1 s1-eth2:s3-eth1 s1-eth3:s4-eth1 s1-eth4:s5-eth1 s1-eth5:h10-eth0
s2 lo:  s2-eth1:s1-eth1 s2-eth2:h1-eth0 s2-eth3:h2-eth0
s3 lo:  s3-eth1:s1-eth2 s3-eth2:h3-eth0 s3-eth3:h4-eth0
s4 lo:  s4-eth1:s1-eth3 s4-eth2:h5-eth0 s4-eth3:h6-eth0
s5 lo:  s5-eth1:s1-eth4 s5-eth2:h7-eth0 s5-eth3:h8-eth0 s5-eth4:h9-eth0
c0
'''

#5 switches
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0
s5_dpid=0

#S1 tem 5 links
s1_p1=0
s1_p2=0
s1_p3=0
s1_p4=0
s1_p5=0

#S2 tem 3 links
s2_p1=0
s2_p2=0
s2_p3=0

#S3 tem 3 links
s3_p1=0
s3_p2=0
s3_p3=0

#S4 tem 3 links
s4_p1=0
s4_p2=0
s4_p3=0

#S5 tem 4 links
s5_p1=0
s5_p2=0
s5_p3=0
s5_p4=0

########### pt2 pre
#S1 tem 5 links
pre_s1_p1=0
pre_s1_p2=0
pre_s1_p3=0
pre_s1_p4=0
pre_s1_p5=0

#S2 tem 3 links
pre_s2_p1=0
pre_s2_p2=0
pre_s2_p3=0

#S3 tem 3 links
pre_s3_p1=0
pre_s3_p2=0
pre_s3_p3=0

#S4 tem 3 links
pre_s4_p1=0
pre_s4_p2=0
pre_s4_p3=0

#S5 tem 4 links
pre_s5_p1=0
pre_s5_p2=0
pre_s5_p3=0
pre_s5_p4=0

#again , idk
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0
s5_dpid=0

########################################

def _handle_portstats_received(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
    global s1_p1, s1_p2, s1_p3, s1_p4, s1_p5, s2_p1, s2_p2, s2_p3, s3_p1, s3_p2, s3_p3, s4_p1, s4_p2, s4_p3, s5_p1, s5_p2, s5_p3, s5_p4
    global pre_s1_p1, pre_s1_p2, pre_s1_p3, pre_s1_p4, pre_s1_p5, pre_s2_p1, pre_s2_p2, pre_s2_p3, pre_s3_p1, pre_s3_p2, pre_s3_p3, pre_s4_p1, pre_s4_p2, pre_s4_p3, pre_s5_p1, pre_s5_p2, pre_s5_p3, pre_s5_p4

    #S1, 5 portas, 1 H-S (rx); 4 S-S (tx)
    if event.connection.dpid == s1_dpid:
        for f in event.stats:
            if int(f.port_no) < 65534:
                if f.port_no == 1:
                    pre_s1_p1 = s1_p1
                    s1_p1 = f.tx_packets
                if f.port_no == 2:
                    pre_s1_p2 = s1_p2
                    s1_p2 = f.tx_packets
                if f.port_no == 3:
                    pre_s1_p3 = s1_p3
                    s1_p3 = f.tx_packets
                if f.port_no == 4:
                    pre_s1_p4 = s1_p4
                    s1_p4 = f.tx_packets
                if f.port_no == 5:
                    pre_s1_p5 = s1_p5
                    s1_p5 = f.rx_packets

    #S2, 3 portas, 2 H-S (rx); 1 S-S (tx)
    if event.connection.dpid == s2_dpid:
        for f in event.stats:
            if int(f.port_no) < 65534:
                if f.port_no == 1:
                    pre_s2_p1 = s2_p1
                    s2_p1 = f.tx_packets
                if f.port_no == 2:
                    pre_s2_p2 = s2_p2
                    s2_p2 = f.rx_packets
                if f.port_no == 3:
                    pre_s2_p3 = s2_p3
                    s2_p3 = f.rx_packets

    #S3, 3 portas, 2 H-S (rx); 1 S-S (tx)
    if event.connection.dpid == s3_dpid:
        for f in event.stats:
            if int(f.port_no) < 65534:
                if f.port_no == 1:
                    pre_s3_p1 = s3_p1
                    s3_p1 = f.tx_packets
                if f.port_no == 2:
                    pre_s3_p2 = s3_p2
                    s3_p2 = f.rx_packets
                if f.port_no == 3:
                    pre_s3_p3 = s3_p3
                    s3_p3 = f.rx_packets

    #S4, 3 portas, 2 H-S (rx); 1 S-S (tx)
    if event.connection.dpid == s4_dpid:
        for f in event.stats:
            if int(f.port_no) < 65534:
                if f.port_no == 1:
                    pre_s4_p1 = s4_p1
                    s4_p1 = f.tx_packets
                if f.port_no == 2:
                    pre_s4_p2 = s4_p2
                    s4_p2 = f.rx_packets
                if f.port_no == 3:
                    pre_s4_p3 = s4_p3
                    s4_p3 = f.rx_packets
                    
    #S5, 4 portas, 3 H-S (rx); 1 S-S (tx)
    if event.connection.dpid == s5_dpid:
        for f in event.stats:
            if int(f.port_no) < 65534:
                if f.port_no == 1:
                    pre_s5_p1 = s5_p1
                    s5_p1 = f.tx_packets
                if f.port_no == 2:
                    pre_s5_p2 = s5_p2
                    s5_p2 = f.rx_packets
                if f.port_no == 3:
                    pre_s5_p3 = s5_p3
                    s5_p3 = f.rx_packets
                if f.port_no == 4:
                    pre_s5_p4 = s5_p4
                    s5_p4 = f.rx_packets

##############################################

def _handle_ConnectionUp(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
    print ("ConnectionUp: ", dpidToStr(event.connection.dpid))

    for m in event.connection.features.ports:
        if m.name == "s1-eth1":
            s1_dpid = event.connection.dpid
            print ("s1_dpid=", s1_dpid)
        elif m.name == "s2-eth1":
            s2_dpid = event.connection.dpid
            print ("s2_dpid=", s2_dpid)
        elif m.name == "s3-eth1":
            s3_dpid = event.connection.dpid
            print ("s3_dpid=", s3_dpid)
        elif m.name == "s4-eth1":
            s4_dpid = event.connection.dpid
            print ("s4_dpid=", s4_dpid)
        elif m.name == "s5-eth1":
            s5_dpid = event.connection.dpid
            print ("s5_dpid=", s5_dpid)

def _handle_PacketIn(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
    packet = event.parsed
    print ("_handle_PacketIn is called, packet.type:", packet.type, " event.connection.dpid:", event.connection.dpid)

#############################################################
#TODO: Add Flows for each switch.
# Connection S1
    if event.connection.dpid == s1_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
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
        if a and a.protodst == "10.0.0.7":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.8":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.9":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.10":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=5))
            event.connection.send(msg)

# AddFlows S1

        ################## S1-from-Host1 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)          


        ################## S1-from-Host2 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host3 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host4 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host5 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host6 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host7 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host8 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host9 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        ################## S1-from-Host10 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

# Connection S2
    if event.connection.dpid == s2_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
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
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.7":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.8":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.9":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.10":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)  

        ################## S2-from-Host1 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        ################## S2-from-Host2 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)                    

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)  

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)   

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        ################## S2-to-Host1 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        ################## S2-to-Host2 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=3))         

# Connection S3
    if event.connection.dpid == s3_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.7":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.8":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.9":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.10":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        
        ################## S3-from-Host3 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))

        ################## S3-from-Host4 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))
        ################## S3-to-Host3 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))

        ################## S3-to-Host4 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))
        
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))

# Connection S4
    if event.connection.dpid == s4_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.7":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.8":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.9":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.10":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        ################## S4-from-Host5 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))

        ################## S4-from-Host6 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))

        ################## S4-to-Host5 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=2))

        ################## S4-to-Host6 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=3))

# Connection S5
    if event.connection.dpid == s5_dpid:
        a = packet.find('arp')
        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.7":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.8":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.9":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)
        if a and a.protodst == "10.0.0.10":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        ################## S5-from-Host7 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.7"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))


        ################## S5-from-Host8 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.8"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))

        ################## S5-from-Host9 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=1))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.9"
        msg.match.nw_dst = "10.0.0.10"
        msg.actions.append(of.ofp_action_output(port=1))

        ################## S5-to-Host7 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.7"
        msg.actions.append(of.ofp_action_output(port=2))


        ################## S5-to-Host8 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.8"
        msg.actions.append(of.ofp_action_output(port=3))

        ################## S5-to-Host9 ###################################
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.1"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.2"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.3"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.4"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.5"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.6"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_src = "10.0.0.10"
        msg.match.nw_dst = "10.0.0.9"
        msg.actions.append(of.ofp_action_output(port=4))

###############################################################################


def launch():
    core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

        