import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

# Parameters
load_dotenv()
unifi_host = os.getenv("UNIFI_HOST")
unifi_user = os.getenv("UNIFI_USER")
unifi_pass = os.getenv("UNIFI_PASS")
unlimited_group_id = os.getenv('UNLIMITED_GROUP_ID')
limited_group_id = os.getenv('LIMITED_GROUP_ID')
wlan_id = os.getenv('WLAN_ID')

# Suppress the HTTPS verification warning globally
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Start a session to persist the cookie
session = requests.Session()

def auth():
    session.cookies.clear()
    session.headers.clear()
    login_data = {
        'username': unifi_user,
        'password': unifi_pass
    }
    # Convert the payload to a JSON string
    json_login_data = json.dumps(login_data)
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        # Post the login data to the login URL
        response = session.post(unifi_host + '/api/auth/login', data=json_login_data, headers=headers, verify=False)

        # Check if the login was successful
        if response.status_code == 200:
            print("Auth successful")
        else:
            raise Exception('ERROR auth(): ' + response.reason + response.text)

        if response.headers.get('X-CSRF-Token'):
            return response.headers.get('X-CSRF-Token')
        else:
            raise Exception('Response did not return X-CSRF-Token')
    except Exception as err:
        print(err)
        exit()


def change_wlan_usergroup(wlan_id, usergroup_id):
    csrf_token = auth()
    api_url = unifi_host + '/proxy/network/api/s/default/rest/wlanconf/' + wlan_id
    wlan_data = {
        'usergroup_id': usergroup_id
    }
    # Convert the payload to a JSON string
    json_wlan_data = json.dumps(wlan_data)
    headers = {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrf_token
    }
    try:
        response = session.put(api_url, data=json_wlan_data, headers=headers, verify=False)
        
        if response.status_code == 200:
            # Get the current timestamp
            current_timestamp = datetime.now()
            formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"WLAN {wlan_id} config updated. usergroup_id: {usergroup_id} ({formatted_timestamp})")
        else:
            raise Exception('ERROR change_wlan_usergroup(): ' + response.reason + response.text)
            
    except Exception as err:
        print(err)
        exit()


# Schedule the job
schedule.every().sunday.at("03:00").do(change_wlan_usergroup, wlan_id=wlan_id, usergroup_id=limited_group_id)  # Every Sunday 3:00 AM
schedule.every().sunday.at("23:00").do(change_wlan_usergroup, wlan_id=wlan_id, usergroup_id=unlimited_group_id)  # Every Sunday 11:00 PM

while True:
    schedule.run_pending()
    time.sleep(1)

