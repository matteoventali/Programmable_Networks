# HANDSON-4 solution
# Student id: 1985026

from device_info import devices
from ncclient import manager
import xmltodict

# Query device info method
def query_device(device):
    with manager.connect(host=device['address'],
                         port=device['port'],
                         username=device['username'],
                         password=device['password'],
                         hostkey_verify=False) as m:

        # Get Configuration and State Info for Interface
        netconf_reply = m.get(netconf_filter)

        # Process the XML and store in useful dictionaries
        intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
        intf_config = intf_details["interfaces"]["interface"]
        
        ifaces_list = []

        for interface in intf_config:
            ifaces_list.append(interface['name'])

        return ifaces_list
            

# NETCONF filter to use
netconf_filter = open("my-filter-ietf-interfaces.xml").read()

if __name__ == '__main__':
    # Scanning all the devices
    for device in devices:
        print(f"Querying device {device['address']}:{device['port']}")
        iface_names = query_device(device)
        print(f"Interfaces name: {iface_names}")
        print("-----")