# unifios-network-scheduler
Schedules the WiFi speed limit on a specified network to assist with live streams. Hardcoded to restrict the network every Sunday 3:00 AM and then remove the restriction at 11:00PM.

Required environment variables:
```
TZ = 'Australia/Sydney'
UNIFI_HOST = 'https://192.168.1.1:443'
UNIFI_USER = 'apiuser'
UNIFI_PASS = 'apipassword'
UNLIMITED_GROUP_ID = '62d761b2'
LIMITED_GROUP_ID = '66ca4c46d'
WLAN_ID = '66c7fea'
```