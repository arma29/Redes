# ext/myfirstapp.py

# Exec
# cd pox/
# python pox.py --verbose myfirstapp py\log --no-default --file=/tmp/mylog.log

'''
EXEC 1
same log
sudo mn --topo single,4 --mac --arp --controller remote
pox> import pox.openflow.libopenflow_01 as of
pox> from myfirstapp import myfirstapp
pox>
pox> msg = of.ofp_flow_mod()
pox> msg.match.in_port = 1
pox> msg.actions.append(of.ofp_action_output(port = 3))
pox> myfirstapp.switches[1].send(msg)
pox>
pox> msg = of.ofp_flow_mod()
pox> msg.match.in_port = 3
pox> msg.actions.append(of.ofp_action_output(port = 1))
pox> myfirstapp.switches[1].send(msg)
pox> 
'''


#import
from pox.core import core
import pox.openflow.libopoenflow_01 as of 
from pox.lib.revent import *

log = core.getLogger()

class myfirstapp(EventMixin):
    switches = {}

    def __init__(self):
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self,event):
        log.debug("Connectin UP from %s", event.dpid)
        myfirstapp.switches[event.dpid] = event.connection
    
    def _handle_PacketIn(self,event):
        pass

def launch ():
    core.openflow.miss_send_len = 1024
    core.registerNew(myfirstapp)