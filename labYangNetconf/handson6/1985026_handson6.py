# HANDSON-6 solution
# Student id: 1985026

from device_info import devices
from ncclient import manager
import xmltodict

OSPF_CONFIG_TEMPLATE = "ospf_template.xml"

# Query device info method
def config_device(device):
    with manager.connect(host=device['address'],
                         port=device['port'],
                         username=device['username'],
                         password=device['password'],
                         hostkey_verify=False) as m:
        
        # Filling the template for the device
        filled_config = netconf_template.format(
                        process_id=device["ospf_processId"],
                        ip_address=device["ospf_ip"],
                        wildcard_mask=device["ospf_wildcard"],
                        area=device["ospf_area"],
                    )
        
        print(filled_config)

        reply = m.edit_config(filled_config, target='running')
        return reply.ok
            

# NETCONF configuration template to be used
netconf_template = open(OSPF_CONFIG_TEMPLATE).read()

if __name__ == '__main__':
    # Scanning all the devices
    for device in devices:
        print(f"Configuring device {device['address']}:{device['port']}")
        success_flag = config_device(device)
        if success_flag:
            print("Configuration applied successfully")
        else:
            print("Configuration task failed")