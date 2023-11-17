import requests
import json
import faker

import meraki_config


MERAKI_API_KEY = meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config

def create_networks():
    url = f"https://{MERAKI_URL}/organizations/{MERAKI_ORG}/networks"
    for network_layout in NETWORK_LAYOUTS:
        # create new network
        resp = requests.post(
            url,
            headers={
                'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
                'Content-Type': "application/json"
            },
            data=json.dumps({
                'name': network_layout['network'],
                'productTypes': "wireless switch appliance camera".split(" "),
                'tags': [faker.Faker().safe_color_name() for _ in range(5)],
                'notes': faker.Faker().text()
            })
        )
        
        newNetworkId = resp.json()['id']

        # claim devices for this network
        url = f"https://{MERAKI_URL}/networks/{newNetworkId}/devices/claim"
        resp = requests.post(
            url,
            headers={
                'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
                'Content-Type': "application/json"
            },
            data=json.dumps({
                # sending all devices serial numbers at once as a list
                'serials': [device['serial'] for device in network_layout['devices']]
            })
        )
        

if __name__=="__main__":
    create_networks()