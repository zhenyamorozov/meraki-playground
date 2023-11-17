import requests
from prettytable import PrettyTable

import meraki_config

MERAKI_API_KEY = meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config

status_table = PrettyTable()
status_table.field_names = ["Serial",
                            "MAC",
                            "Model",
                            "LAN IP",
                            "Product Type",
                            "Public IP1",
                            "Public IP2"]

# Get all devices in the org
def print_org_devices():
    url = f"https://{MERAKI_URL}/organizations/{MERAKI_ORG}/devices"

    resp = requests.get(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application-json"

        }
    )

    for device in resp.json():
        status_table.add_row([
            device['serial'],
            device['mac'],
            device['model'],
            device['productType'],
            device['lanIp'] if 'lanIp' in device else "N/A",
            "N/A",
            "N/A"
        ])

    print(status_table)

if __name__=="__main__":
    print_org_devices()