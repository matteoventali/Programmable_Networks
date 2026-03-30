from pox.lib.revent import Event

# Custom event
class InPktSeen (Event):
    def __init__(self):
        Event.__init__(self)