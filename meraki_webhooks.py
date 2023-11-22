import requests
import json

import meraki_config

MERAKI_API_KEY = meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config

# List all networks in org
def get_networks():
    url = f"https://{MERAKI_URL}/organizations/{MERAKI_ORG}/networks"
    resp = requests.get(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        }
    )
    return resp.json()


# Create a webhook HTTP receiver for a network
def create_webhook_httpServer(network_id, server_name, server_url, secret=""):
    url = f"https://{MERAKI_URL}/networks/{network_id}/webhooks/httpServers"

    resp = requests.post(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        },
        data=json.dumps({
            'name': server_name,
            'url': server_url,
            'sharedSecret': secret
        })
    )
    return resp.json()

# Delete webhook HTTP receiver for a network
def delete_webhook_httpServer(network_id, httpReceiver_id):
    url = f"https://{MERAKI_URL}/networks/{network_id}/webhooks/httpServers/{httpReceiver_id}"

    resp = requests.delete(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        }
    )

# Get current alerts settings, including configured receivers and webhooks
def get_alert_settings(network_id):

    url = f"https://{MERAKI_URL}/networks/{network_id}/alerts/settings"

    resp = requests.get(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application-json"
        }
    )
    return resp.json()

# Set HTTP webhooks receiver as default destination in alert settings
def set_alert_receiver(network_id, httpServer_id):
    url = f"https://{MERAKI_URL}/networks/{network_id}/alerts/settings"

    resp = requests.put(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        },
        data=json.dumps({
            'defaultDestinations': {
                'httpServerIds': [
                    httpServer_id
                ]
            }
        })
    )
    return resp.json()

# turn on alerts for specific event types
def set_alerts(network_id, alerts=[]):
    url = f"https://{MERAKI_URL}/networks/{network_id}/alerts/settings"

    resp = requests.put(
        url,
        headers={
            'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
            'Content-Type': "application/json"
        },
        data=json.dumps({
            'alerts':[
                {'type':alert, 'enabled': True} for alert in alerts
            ]
        })
    )
    return resp.json()


if __name__=="__main__":

    # get a network ID to play with
    network_id = get_networks()[0]['id']

    # print currently configured alert settings
    alert_settings = get_alert_settings(network_id)
    print(json.dumps(alert_settings, indent=4))

    # print list of possible alert types
    print([alert['type'] for alert in alert_settings['alerts']])

    # create a new webhook receiver
    httpServer = create_webhook_httpServer(network_id, "My local webhook receiver", "https://cisco.com:5000/test", secret="topsecret")
    print(json.dumps(httpServer, indent=4))

    # set this httpServer as webhooks receiver
    alert_settings = set_alert_receiver(network_id, httpServer['id'])

    # turn on specific alert types
    alert_settings = set_alerts(network_id, ["rogueAp", "gatewayDown", "settingsChanged"])
    
    # request and again, print currently configured alert settings
    print(json.dumps(get_alert_settings(network_id)['defaultDestinations'], indent=4))

    # clean up - delete webhook HTTP server
    delete_webhook_httpServer(network_id, httpServer['id'])

    # is alert settings still pointing to the (now deleted) httpServerID ??   - NO, it is also cleaned up, good!
    print(json.dumps(get_alert_settings(network_id)['defaultDestinations'], indent=4))    



    