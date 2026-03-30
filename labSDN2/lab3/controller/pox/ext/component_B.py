from pox.core import core
from pox.lib import revent

class ComponentB (object):
   
    def __init__ (self):
      # Subscribing the component B in order to receive
      # the events of componentA
      core.componentA.addListeners(self)
      
    # Handler for the event inPktSeen
    def _handle_InPktSeen (self, event):
      # Printing a message onto the screen
      print("I'm component B: packet A has raised InPktSeen")


def launch ():
   component = ComponentB()
   core.register("componentB", component)