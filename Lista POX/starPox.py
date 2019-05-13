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


