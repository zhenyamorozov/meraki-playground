import requests
import json
import meraki_config


MERAKI_API_KEY = meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config
GROUP_POLICY = meraki_config.group_policy_json
VLANS = meraki_config.vlans_json



def configure_networks():
    # Get all networks in org
    url = f"https://{MERAKI_URL}/organizations/{MERAKI_ORG}/networks"
    resp = requests.get(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        }
    )
    
    # Configure Group Policy and VLANs for all networks in the org 
    for network in resp.json():
        # assign group policy to network
        url = f"https://{MERAKI_URL}/networks/{network['id']}/groupPolicies"
        resp = requests.post(
            url,
            headers={
                'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
                'Content-Type': "application/json"
            },
            data=GROUP_POLICY
        )

        # enable VLANs in the network
        url = f"https://{MERAKI_URL}/networks/{network['id']}/appliance/vlans/settings"
        resp = requests.put(
            url,
            headers={
                'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
                'Content-Type': "application/json"
            },
            data=json.dumps({'vlansEnabled': True})
        )
        

        # assign VLANs to network
        url = f"https://{MERAKI_URL}/networks/{network['id']}/appliance/vlans"
        for vlan in VLANS:
            resp = requests.post(
                url,
                headers={
                    'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
                    'Content-Type': "application/json"
                },
                data=vlan
            )

        


if __name__=="__main__":
    configure_networks()


