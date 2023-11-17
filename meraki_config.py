# import os
# lab_description = os.popen('vmtoolsd --cmd="info-get guestinfo.lasaction.1"').read()

from dotenv import dotenv_values
lab_description = dotenv_values(".env")["LAB_DESCRIPTION"]

lab_description = lab_description.replace('set_computer_description~~','')
lab_description = lab_description.replace('\n','')
lab_description = lab_description.split(',')

merakiapikey = lab_description[7]
merakiorg = lab_description[6]
merakiurl = "api.meraki.com/api/v1"
merakimx = lab_description[3]
merakims = lab_description[4]
merakimr = lab_description[5]

net_device_config = [
    {
     "network": "ENAUI",
        "devices": [
           {"serial": merakimx},
           {"serial": merakims},
           {"serial": merakimr},
       ]
   }
]

vlans_json = [
    """
    {
      "id": "10",
      "name": "Meraki_VLAN_10",
      "subnet": "192.168.10.0/24",
      "applianceIp": "192.168.10.1"
    }
    """,
    """
    {
      "id": "11",
      "name": "Meraki_VLAN_11",
      "subnet": "192.168.11.0/24",
      "applianceIp": "192.168.11.1"
    }
    """,
    """
    {
      "id": "12",
      "name": "Meraki_VLAN_12",
      "subnet": "192.168.12.0/24",
      "applianceIp": "192.168.12.1"
    }
    """,
    """
    {
      "id": "13",
      "name": "Meraki_VLAN_13",
      "subnet": "192.168.13.0/24",
      "applianceIp": "192.168.13.1"
    }
    """,
]

group_policy_json = """
    {
        "name": "GP_1",
        "scheduling": {
            "enabled": true,
            "monday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "tuesday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "wednesday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "thursday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "friday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "saturday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            },
            "sunday": {
                "active": true,
                "from": "00:00",
                "to": "24:00"
            }
        },
        "bandwidth": {
            "settings": "custom",
            "bandwidthLimits": {
                "limitUp": 25600,
                "limitDown": 25600
            }
        },
        "firewallAndTrafficShaping": {
            "settings": "custom",
            "trafficShapingRules": [],
            "l3FirewallRules": [
                {
                    "comment": "Block SSL",
                    "policy": "deny",
                    "protocol": "tcp",
                    "destPort": "443",
                    "destCidr": "10.10.10.10/32"
                },
                {
                    "comment": "Block SSH",
                    "policy": "deny",
                    "protocol": "tcp",
                    "destPort": "22",
                    "destCidr": "10.10.10.20/32"
                }
            ],
            "l7FirewallRules": [
                {
                    "policy": "deny",
                    "type": "application",
                    "value": {
                        "id": "meraki:layer7/application/189",
                        "name": "Blizzard"
                    }
                },
                {
                    "policy": "deny",
                    "type": "applicationCategory",
                    "value": {
                        "id": "meraki:layer7/category/27",
                        "name": "Advertising"
                    }
                }
            ]
        },
        "splashAuthSettings": "network default",
        "vlanTagging": {
            "settings": "network default"
        },
        "bonjourForwarding": {
            "settings": "network default",
            "rules": []
        }
    }
"""

