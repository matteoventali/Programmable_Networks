from device_info import ios_xe1
from ncclient import manager
import xmltodict


netconf_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
        <routing-instance>
            <name>default</name>
            <ribs>
                <rib>
                    <name>ipv4-default</name>
                    <routes>
                        <route>
                            <destination-prefix>
                            </destination-prefix>
                            <next-hop>
                            </next-hop>
                        </route>
                    </routes>
                </rib>
            </ribs>
        </routing-instance>
    </routing-state>
</filter>
"""


if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"],
                         port=ios_xe1["port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as m:

        # Get Configuration and State Info for Interface
        netconf_reply = m.get(netconf_filter)

        intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]["routing-state"]["routing-instance"]["ribs"]["rib"]["routes"]["route"]
        print(intf_details[0]["destination-prefix"])
        print(intf_details[0]["next-hop"]["outgoing-interface"])
        print(intf_details[0]["next-hop"]["next-hop-address"])
