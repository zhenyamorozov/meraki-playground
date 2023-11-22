from flask import Flask, request
import requests
import json

import meraki_config
import meraki_webhooks

MERAKI_API_KEY = meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config

# get public URL from ngrok
resp = requests.get("http://localhost:4040/api/tunnels")
public_url = resp.json()['tunnels'][0]['public_url']

# get a network ID to play with
network_id = meraki_webhooks.get_networks()[0]['id']

# create HTTP server for Meraki alerts
httpServer = meraki_webhooks.create_webhook_httpServer(
    network_id=network_id,
    server_name="Webhook testing",
    server_url=public_url,
    secret="shhhh"
)

# add webhook receiver
alertSettings = meraki_webhooks.set_alert_receiver(
    network_id=network_id,
    httpServer_id=httpServer['id']
)

# set alert types to trigger webhook
alertSettings = meraki_webhooks.set_alerts(network_id, ["rogueAp", "gatewayDown", "settingsChanged"])


meraki_app = Flask(__name__)

@meraki_app.route("/", methods=["POST"])
def process_alert():

    # if something happened, do something
    # print(json.dumps(request.json, indent=4))
    print(f"Alert ({request.json['alertLevel']}): {request.json['alertType']}")
    if request.json['deviceName'] or request.json['deviceModel']:
        print(f"  at device: {request.json['deviceName']} ({request.json['deviceModel']})")

    return "received"



if __name__=="__main__":
    meraki_app.run(port=5000)