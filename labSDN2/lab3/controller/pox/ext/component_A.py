from pox.core import core
from pox.lib import revent
from customEvents import InPktSeen

class ComponentA (revent.EventMixin):
    
    # Events that can be raised by this component
    _eventMixin_events = set([InPktSeen])

    def __init__ (self):
      revent.EventMixin.__init__(self)
      
      # Subscribing the component A in order to receive
      # the events related to the openflow protocol
      core.openflow.addListeners(self)
      
    # Handler for the event packetIn
    def _handle_PacketIn (self, event):
      # Printing a message onto the screen
      print("I'm component A: packetIn handler")

      # Raising an event of type pktInSeen
      self.raiseEvent(InPktSeen())


def launch ():
   component = ComponentA()
   core.register("componentA", component)