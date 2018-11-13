# ext/poxl2.py
# cd pox/
# python pox.py --verbose poxproj py\log --no-default --file=/tmp/mylog.log

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

