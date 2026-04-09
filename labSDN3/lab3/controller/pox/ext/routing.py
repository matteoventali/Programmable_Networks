import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import dpidToStr
import numpy as np
import networkx as nx

class Routing():

	def __init__(self):
		core.openflow.addListeners(self)
		self.host_location = {}
		self.host_ip_mac = {}
		self.max_hosts = 5

	def _handle_ConnectionUp(self, event):
		self.hostDiscovery(event.connection)

	def hostDiscovery(self, connection):
		for h in range(self.max_hosts):
			arp_req = arp()
			arp_req.hwsrc = EthAddr("00:00:00:00:11:11")
			arp_req.opcode = arp.REQUEST
			arp_req.protosrc = IPAddr("10.0." + str(h) + ".1")
			arp_req.protodst = IPAddr("10.0." + str(h) + ".100")
			ether = ethernet()
			ether.type = ethernet.ARP_TYPE
			ether.dst = EthAddr.BROADCAST
			ether.src = EthAddr("00:00:00:00:11:11")
			ether.payload = arp_req
			msg = of.ofp_packet_out()
			msg.data = ether.pack()
			msg.actions.append(of.ofp_action_output(port = 1))
			connection.send(msg)

	def _handle_PacketIn(self, event):
		eth_frame = event.parsed
		output_log = ""

		if eth_frame.type == ethernet.ARP_TYPE and eth_frame.dst == EthAddr("00:00:00:00:11:11"):
			arp_msg = eth_frame.payload
			if arp_msg.opcode == arp.REPLY:
				ip_host = arp_msg.protosrc.toStr()
				mac_host = arp_msg.hwsrc.toStr()
				dpid = dpidToStr(event.dpid)
				self.host_location[ip_host] = event.dpid
				self.host_ip_mac[ip_host] = mac_host
		elif eth_frame.type == ethernet.IP_TYPE:
			ip_pkt = eth_frame.payload
			ip_src = ip_pkt.srcip
			ip_dst = ip_pkt.dstip
			switch_src = self.host_location[ip_src.toStr()]
			switch_dst = self.host_location[ip_dst.toStr()]
			S = list(core.linkDiscovery.switch_id.keys())[list(core.linkDiscovery.switch_id.values()).index(switch_src)]
			D = list(core.linkDiscovery.switch_id.keys())[list(core.linkDiscovery.switch_id.values()).index(switch_dst)]

			output_log = f"Ip packet from {ip_src} to {ip_dst} from switch {S} to {D}"

			graph = core.linkDiscovery.getGraph()
			path = nx.shortest_path(graph, S, D)
			#print(path)
			output_log = output_log + f"\nPath: {path}"
			print(output_log)
			self.install_path(path, ip_src, ip_dst)

	''' Method to install the flow rules across following the path
		Assuming we have a list ['s1', ..., 's_i', s_j', ...] we must:
		- match the IP packet trough ip_src and ip_dst;
		- install a rule that forward the IP packet (matched) from s_i to s_j
		- when the next hop is the last node into the path, on this node we must forward the packet
		  to the port connected with the host 
	'''
	def install_path(self, path, ip_src, ip_dst):
		
		def node_to_sid(node):
			return int(node.replace('s', ''))

		def get_out_port(sid_a, sid_b):
			for link in core.linkDiscovery.links.values():
				if link.sid1 == sid_a and link.sid2 == sid_b:
					return link.port1
				if link.sid1 == sid_b and link.sid2 == sid_a:
					return link.port2
			return None

		# Installing the flow rules
		for i in range(len(path) - 1):
			sid_curr = node_to_sid(path[i])
			sid_next = node_to_sid(path[i + 1])

			out_port = get_out_port(sid_curr, sid_next)
			if out_port is None:
				continue

			dpid = core.linkDiscovery.switch_id[sid_curr]
			conn = core.openflow.getConnection(dpid)
			if conn is None:
				continue

			fm = of.ofp_flow_mod()
			fm.priority = 100

			fm.match.dl_type = ethernet.IP_TYPE
			fm.match.nw_src = IPAddr(ip_src)
			fm.match.nw_dst = IPAddr(ip_dst)

			fm.idle_timeout = 10
			fm.hard_timeout = 30

			fm.actions.append(of.ofp_action_output(port=out_port))
			conn.send(fm)

		# Last hop into the path
		last_sid = node_to_sid(path[-1])
		dpid_last = core.linkDiscovery.switch_id[last_sid]
		conn_last = core.openflow.getConnection(dpid_last)

		if conn_last is not None and ip_dst in self.host_location:
			(_, host_port) = self.host_location[ip_dst]

			fm = of.ofp_flow_mod()
			fm.priority = 100
			fm.match.dl_type = ethernet.IP_TYPE
			fm.match.nw_src = IPAddr(ip_src)
			fm.match.nw_dst = IPAddr(ip_dst)

			fm.actions.append(of.ofp_action_output(port=host_port))
			conn_last.send(fm)

def launch():
	Routing()
