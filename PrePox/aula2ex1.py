'''
EXEC 2
sudo mn --topo single,4 --mac --arp --controller remote
'''

# ext/aula2ex1.py

#import
from pox.core import core
import pox.openflow.libopoenflow_01 as of 
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpidToStr

log = core.getLogger()

class aula2ex1(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self,event):
        log.debug("Connectin UP from %s", event.dpid)
    
    def _handle_PacketIn(self,event):
        packet = event.parsed
        #Drop
        msg = of.ofp_flow_mod()
        msg.match.in_port = event.port
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        event.connection.send(msg)
        #Talvez esteja errado
        log.debug("Drop packet sw=%s in_port%s src=%s dst=%s", event.dpid, event.port, packet.src, packet.dst) 

def launch ():
    core.openflow.miss_send_len = 1024
    core.registerNew(aula2ex1)