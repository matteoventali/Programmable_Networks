# HANDSON-5 solution
# Student id: 1985026

from device_info import devices
from ncclient import manager
import xmltodict
import time

T = 5 # Timeout interval for scanning all the devices
FILTER_PATH = "1985026_handson5.xml"

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
        answer_payload = intf_details["interfaces-state"]["interface"]
        
        answer = []

        for interface in answer_payload:
            answer.append({
                "name":interface["name"],
                "pkts":interface["statistics"]["out-unicast-pkts"],
                "bytes":interface["statistics"]["out-octets"]
            })
            
        return answer

# Scanning devices method
def scan_devices(devices):          
    # Scanning all the devices
    for device in devices:
        print(f"Querying device {device['address']}:{device['port']}")
        ifaces_stats = query_device(device)
        for iface in ifaces_stats:
            print(f"Interface: {iface['name']}")
            print(f"Pkts: {iface['pkts']}")
            print(f"Bytes: {iface['bytes']}")
        print("-----")

# NETCONF filter to use
netconf_filter = open(FILTER_PATH).read()

if __name__ == '__main__':
    while True:
        scan_devices(devices)
        time.sleep(T)