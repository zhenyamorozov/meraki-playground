""" This sample utilizes Meraki Python Library
It performs several operations with Meraki API: 
requests information, checks and updates settings
for an SSID and Splash Page configuration.
It implements an external EXCAP splash page flow.
"""

import meraki

import meraki_config

from flask import Flask, request, redirect, url_for
from urllib.parse import urlencode
import requests

from dotenv import dotenv_values


MERAKI_API_KEY = dotenv_values(".env")["MERAKI_API_KEY"]  #meraki_config.merakiapikey
MERAKI_ORG = meraki_config.merakiorg
MERAKI_URL = meraki_config.merakiurl
NETWORK_LAYOUTS = meraki_config.net_device_config

# get public URL from ngrok
public_url = requests.get("http://localhost:4040/api/tunnels").json()['tunnels'][0]['public_url']


meraki_app = Flask(__name__)

@meraki_app.route("/", methods=["GET"])
def root():
    return redirect(url_for("splash"), 307)

@meraki_app.route("/splash", methods=["GET"])
def splash():
    print("Splash page requested")
    print(f"New user registers with IP: {request.args['client_ip']}  MAC: {request.args['client_mac']}")


    return """<h1>This is the splash page</h1>
    <p>Your soul now belongs to me</p>
    <a href="{}">Clck to agree and proceed</a>
    
    """.format(request.args['base_grant_url'] + "?" + urlencode({'continue_url':request.args['user_continue_url'] }))



if __name__=="__main__":

    # init Meraki Dashboard API 
    merakiApi = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)

    # list orgs and grab one specific
    orgs = merakiApi.organizations.getOrganizations()
    org = next(org for org in orgs if org['name']=="Barcelona Co-Innovation Center")

    # grab a network to play with
    network = merakiApi.organizations.getOrganizationNetworks(org['id'])[0]

    # list network wireless SSIDs
    ssids = merakiApi.wireless.getNetworkWirelessSsids(networkId=network['id'])

    # grab an SSID with a specific name
    ssid = next(ssid for ssid in ssids if "SplashTest" in ssid['name'] )

    # make sure SSID is enabled
    ssid = merakiApi.wireless.updateNetworkWirelessSsid(
        networkId=network['id'],
        number=ssid['number'],
        enabled=True,
        authMode="open"
        
    )

    # enable use of Splash page for this SSID
    ssidSettings = merakiApi.wireless.updateNetworkWirelessSsid(
        networkId=network['id'],
        number=ssid['number'],
        splashPage="Click-through splash page"  # must be the specific string
    )

    # get current SSID Splash setings
    splashSettings = merakiApi.wireless.getNetworkWirelessSsidSplashSettings(networkId=network['id'], number=ssid['number'])

    # set Splash settings
    splashSettings = merakiApi.wireless.updateNetworkWirelessSsidSplashSettings(
        networkId=network['id'],
        number=ssid['number'],
        splashUrl=public_url+"/splash",
        useSplashUrl=True,
        redirectUrl="https://meraki.cisco.com",
        useRedirectUrl=True,
        welcomeMessage="Welcome!"
    )

    pass




    meraki_app.run(port=5000)