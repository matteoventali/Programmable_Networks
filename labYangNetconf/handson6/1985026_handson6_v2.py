# HANDSON-6_v2 solution
# Student id: 1985026

from device_info_v2 import devices
from ncclient import manager
from db_ospf_v2 import configs
import xmltodict


OSPF_CONFIG_TEMPLATE = "ospf_template.xml"

# Query device info method
def config_device(device):
    with manager.connect(host=device['address'],
                         port=device['port'],
                         username=device['username'],
                         password=device['password'],
                         hostkey_verify=False) as m:
        
        # Retrieving all the config objects related to the same
        # device (the current one)
        device_configs = [item for item in configs if item["device_id"] == device["device_id"]]
        results = []

        # Filling the template for the device
        for c in device_configs:
            filled_config = netconf_template.format(
                            process_id=c["ospf_processId"],
                            ip_address=c["ospf_ip"],
                            wildcard_mask=c["ospf_wildcard"],
                            area=c["ospf_area"],
                        )
            print(filled_config)
            reply = m.edit_config(filled_config, target='running')
            results.append(reply.ok)
        
        return results
    
        
# NETCONF configuration template to be used
netconf_template = open(OSPF_CONFIG_TEMPLATE).read()

if __name__ == '__main__':
    # Scanning all the devices
    for device in devices:
        print(f"Configuring device {device['address']}:{device['port']}")
        results_obtained = config_device(device)
        if all(results_obtained):
            print("Configuration applied successfully")
        else:
            print("Configuration task failed")