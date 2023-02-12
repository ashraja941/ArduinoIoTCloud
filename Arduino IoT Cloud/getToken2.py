import os
import time
import json 

import iot_api_client as iot

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


#CLIENT_ID = os.getenv("CLIENT_ID")  # get a valid one from your Arduino Create account
#CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # get a valid one from your Arduino Create account

def startApi():
    CLIENT_ID = "OJDD9Vl0SjBFF1GhkLZg2LlKfTm6nqwK"
    CLIENT_SECRET = "4yYtn7dZyPI8xsNbEdoNJaiXgspP3scPzf6rS7WY8AUxJ4qPfAzJoqEeZ2pdifvK"
    # Setup the OAuth2 session that'll be used to request the server an access token
    oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"
    oauth = OAuth2Session(client=oauth_client)

    # This will fire an actual HTTP call to the server to exchange client_id and
    # client_secret with a fresh access token
    token = oauth.fetch_token(
        token_url=token_url,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )

    # If we get here we got the token, print its expiration time
    print("Got a token, expires in {} seconds".format(token.get("expires_in")))

    # Now we setup the iot-api Python client, first of all create a
    # configuration object. The access token goes in the config object.
    client_config = iot.Configuration(host="https://api2.arduino.cc/iot")
    # client_config.debug = True
    client_config.access_token = token.get("access_token")    
    return client_config

    
def getValue(client_config):
    # Create the iot-api Python client with the given configuration
    client = iot.ApiClient(client_config)

    # Each API model has its own wrapper, here we want to interact with
    # devices, so we create a DevicesV2Api object
    devices = iot.DevicesV2Api(client)
    properties = iot.PropertiesV2Api(client)

    # Get a list of devices, catching the specific exception
    try:
        resp = devices.devices_v2_list()
        print("Response from server:")
        #print(resp)
        temp = properties.properties_v2_show("77a8f44a-b7a3-476e-91ce-55dfb9735f61","cc8b2dfe-bd85-47b6-a69b-914761e6d877")
        print(temp.last_value)

    except iot.ApiException as e:
        print("An exception occurred: {}".format(e))

    return temp.last_value


