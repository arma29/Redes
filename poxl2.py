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

#5 switches
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0
s5_dpid=0

#S1 tem 6 links
s1_p1=0
s1_p2=0
s1_p3=0
s1_p4=0
s1_p5=0
s1_p6=0

#S5 tem 4 links
s5_p1=0
s5_p2=0
s5_p3=0
s5_p4=0

#S2 tem 3 links
s2_p1=0
s2_p2=0
s2_p3=0

#S4 tem 3 links
s4_p1=0
s4_p2=0
s4_p3=0

#S3 tem 2 links (no hosts)
s3_p1=0
s3_p2=0

########### pt2 pre
#S1 tem 6 links
pre_s1_p1=0
pre_s1_p2=0
pre_s1_p3=0
pre_s1_p4=0
pre_s1_p5=0
pre_s1_p6=0

#S5 tem 4 links
pre_s5_p1=0
pre_s5_p2=0
pre_s5_p3=0
pre_s5_p4=0

#S2 tem 3 links
pre_s2_p1=0
pre_s2_p2=0
pre_s2_p3=0

#S4 tem 3 links
pre_s4_p1=0
pre_s4_p2=0
pre_s4_p3=0

#S3 tem 2 links (no hosts)
pre_s3_p1=0
pre_s3_p2=0

#again
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0
s5_dpid=0

##########

def _handle_portstats_received(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
    global s1_p1 ,s1_p2 ,s1_p3 ,s1_p4 ,s1_p5 ,s1_p6 ,s5_p1 ,s5_p2 ,s5_p3 ,s5_p4 ,s2_p1 ,s2_p2 ,s2_p3 ,s4_p1 ,s4_p2 ,s4_p3 ,s3_p1 ,s3_p2
    global pre_s1_p1 ,pre_s1_p2 ,pre_s1_p3 ,pre_s1_p4 ,pre_s1_p5 ,pre_s1_p6 ,pre_s5_p1 ,pre_s5_p2 ,pre_s5_p3 ,pre_s5_p4 ,pre_s2_p1 ,pre_s2_p2 ,pre_s2_p3 ,pre_s4_p1 ,pre_s4_p2 ,pre_s4_p3 ,pre_s3_p1 ,pre_s3_p2

    #S1 , 6 portas, 3 H-S, 3 S-S, 3 rx (host?) e tx(switch)
    if event.connection.dpid==s1_dpid:
      for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s1_p1=s1_p1
           s1_p1=f.rx_packets
         if f.port_no==2:
           pre_s1_p2=s1_p2
           s1_p2=f.rx_packets
         if f.port_no==3:
           pre_s1_p3=s1_p3
           s1_p3=f.rx_packets
         if f.port_no==4:
           pre_s1_p4=s1_p4
           s1_p4=f.tx_packets
         if f.port_no==5:
           pre_s1_p5=s1_p5
           s1_p5=f.tx_packets
         if f.port_no==6:
           pre_s1_p6=s1_p6
           s1_p6=f.tx_packets
   #S2, 3 portas, 1 rx , 2 tx
    if event.connection.dpid==s2_dpid:
      for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s2_p1=s2_p1
           s2_p1=f.rx_packets
         if f.port_no==2:
           pre_s2_p2=s2_p2
           s2_p2=f.tx_packets
         if f.port_no==3:
           pre_s2_p3=p2_p3
           s2_p3=f.tx_packets

    #S3, 2 portas, 2 tx
    if event.connection.dpid==s3_dpid:
      for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s3_p1=s3_p1
           s3_p1=f.tx_packets
         if f.port_no==2:
           pre_s3_p2=s3_p2
           s3_p2=f.tx_packets

   #S4, 3 portas, 1 rx, 2tx
    if event.connection.dpid==s4_dpid:
      for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s4_p1=s4_p1
           s4_p1=f.rx_packets
         if f.port_no==2:
           pre_s4_p2=s4_p2
           s4_p2=f.tx_packets
         if f.port_no==3:
           pre_s4_p3=s4_p3
           s4_p3=f.tx_packets
    #S5, 4 portas, 1rx, 3 tx
    if event.connection.dpid==s5_dpid:
      for f in event.stats:
       if int(f.port_no)<65534:
         if f.port_no==1:
           pre_s5_p1=s5_p1
           s5_p1=f.rx_packets
         if f.port_no==2:
           pre_s5_p2=s5_p2
           s5_p2=f.tx_packets
         if f.port_no==3:
           pre_s5_p3=p5_p3
           s5_p3=f.tx_packets
         if f.port_no==4:
           pre_s5_p4=p5_p4
           s5_p4=f.tx_packets

###########
def _handle_ConnectionUp (event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
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
     elif m.name == "s4-eth1":
       s4_dpid = event.connection.dpid
       print "s4_dpid=", s4_dpid
     elif m.name == "s5-eth1":
       s5_dpid = event.connection.dpid
       print "s5_dpid=", s5_dpid

def _handle_PacketIn(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid
    packet=event.parsed
    print "_handle_PacketIn is called, packet.type:", packet.type, " event.connection.dpid:", event.connection.dpid

##################################
#Connection s1
    if event.connection.dpid==s1_dpid:
        a=packet.find('arp')
        if a and a.protodst=="10.0.0.1":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=1))
           event.connection.send(msg)
        if a and a.protodst=="10.0.0.2":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=2))
           event.connection.send(msg)
        if a and a.protodst=="10.0.0.3":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=3))
           event.connection.send(msg)
        if a and a.protodst=="10.0.0.4":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=4))
           event.connection.send(msg)
        if a and a.protodst=="10.0.0.5":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=5))
           event.connection.send(msg)
        if a and a.protodst=="10.0.0.6":
           msg = of.ofp_packet_out(data=event.ofp)
           msg.actions.append(of.ofp_action_output(port=6))
           event.connection.send(msg)
#flows s1 basics
    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 4))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 5))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.6"
    msg.actions.append(of.ofp_action_output(port = 6))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.6"
    msg.actions.append(of.ofp_action_output(port = 6))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 4))
    event.connection.send(msg)

######### s2 connection
    if event.connection.dpid==s2_dpid:
       a=packet.find('arp')
       if a and a.protodst=="10.0.0.4":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=1))
          event.connection.send(msg)
       if a and a.protodst=="10.0.0.1":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=2))
          event.connection.send(msg)
       if a and a.protodst=="10.0.0.2":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=2))
          event.connection.send(msg)
       if a and a.protodst=="10.0.0.3":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=2))
          event.connection.send(msg)
       if a and a.protodst=="10.0.0.5":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=3))
          event.connection.send(msg)
       if a and a.protodst=="10.0.0.6":
          msg = of.ofp_packet_out(data=event.ofp)
          msg.actions.append(of.ofp_action_output(port=3))
          event.connection.send(msg)

#Add flows s2
    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.6"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

#####Connection s3
 if event.connection.dpid==s3_dpid:
    a=packet.find('arp')
    if a and a.protodst=="10.0.0.5":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=1))
       event.connection.send(msg)
    if a and a.protodst=="10.0.0.4":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=1))
       event.connection.send(msg)
    if a and a.protodst=="10.0.0.6":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=1))
       event.connection.send(msg)
    if a and a.protodst=="10.0.0.1":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=2))
       event.connection.send(msg)
    if a and a.protodst=="10.0.0.2":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=2))
       event.connection.send(msg)
    if a and a.protodst=="10.0.0.3":
       msg = of.ofp_packet_out(data=event.ofp)
       msg.actions.append(of.ofp_action_output(port=2))
       event.connection.send(msg)

#Add flows s3
    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.2"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.1"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.4"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.5"
    msg.actions.append(of.ofp_action_output(port = 3))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.3"
    msg.match.nw_dst = "10.0.0.6"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_output(port = 2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.4"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.5"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.priority =100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.6"
    msg.match.nw_dst = "10.0.0.3"
    msg.actions.append(of.ofp_action_output(port = 1))
    event.connection.send(msg)
