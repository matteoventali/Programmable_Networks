from device_info import ios_xe1
from ncclient import manager


def main():
    """
    Main method that prints netconf capabilities of device.
    """

    with manager.connect(host=ios_xe1["address"], port=ios_xe1["port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as m:

        rpc = '''
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <router>
                            <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                                <ospf>
                                    <process-id>
                                        <id>1</id>
                                        <network>
                                            <ip>10.1.1.0</ip>
                                            <wildcard>0.255.255.255</wildcard>
                                            <area>0.0.0.0</area>
                                        </network>
                                    </process-id>
                                </ospf>
                            </router-ospf>
                        </router>
                    </native>
                </config>
            '''

        reply = m.edit_config(rpc, target='running')
        print(reply)


if __name__ == '__main__':
    main()
