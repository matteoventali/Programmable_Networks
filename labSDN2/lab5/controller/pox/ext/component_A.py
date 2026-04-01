from pox.core import core
import pox.lib.packet.ethernet as eth
import pox.openflow.libopenflow_01 as of

class ComponentA (object):
    def __init__ (self):
        # Subscribing the component A in order to receive
        # the events related to the openflow protocol
        core.openflow.addListeners(self)

    # Handler for the event packetIn
    def _handle_PacketIn (self, event):
        # Parsing the packet
        packet = event.parsed
        
        # Extracting ethernet frame
        ethernet_frame = packet.find('ethernet')

        print(f"Before swap: src->{ethernet_frame.src} dst->{ethernet_frame.dst}")

        # Swap source and destination mac
        ethernet_frame.src, ethernet_frame.dst = ethernet_frame.dst, ethernet_frame.src

        print(f"After swap: src->{ethernet_frame.src} dst->{ethernet_frame.dst}")

        # Send the frame back with output port the one that has been received
        msg = of.ofp_packet_out()
        msg.data = ethernet_frame
        msg.actions.append(of.ofp_action_output(port = event.port))
        event.connection.send(msg)

def launch ():
    component = ComponentA()
    core.register("componentA", component)