# Created from information at:
#   https://jereze.com/code/authentification-salesforce-rest-api-python/
#   Feb 2020 CCK
#   See EN topic on API for breadcrumbs
#   Set to run with python3 command

import requests
params = {
    "grant_type": "password",
    "client_id": "3MVG9LBJLApeX_PBm1plzeEdrmR4tN4jDinNZyHXLH1XzsDPptaoa.MW1arNvoCg1D7LRN.Sv_3vj3qOCTAzj", # Consumer Key
    "client_secret": "96EF64F80520CDD69C63913639B5AF58543D7AB0506A56C2B3337438DDB52910", # Consumer Secret
    "username": "chris@brave-fox-riktj8.com",
    "password": "sales1forceAVBUvqrdoc7LYFpVRe0Ue9aQ"
}
r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)
