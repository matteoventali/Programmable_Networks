from pox.core import core
from pox.lib import revent
import pox.lib.packet.ethernet as eth

class ComponentA (object):
    def __init__ (self):
        # Subscribing the component A in order to receive
        # the events related to the openflow protocol
        core.openflow.addListeners(self)
      
    # Handler for the event packetIn
    def _handle_PacketIn (self, event):
        # Parsing the packet
        packet = event.parsed
        if packet.type == eth.IP_TYPE:
            print("Component A: IP packet detected")
        else:
            print("Component A: Not an IP packet")

def launch ():
    component = ComponentA()
    core.register("componentA", component)