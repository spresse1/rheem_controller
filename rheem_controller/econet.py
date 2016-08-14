from rheem_auth import RheemAuth

# Base url for the API
BASE_URL = "https://io.myrheem.com"
API_ENDPOINTS = {
    "locations": "/locations",
    "vacations": "/vacations",
    "equipment": "/equipment",
    "remove_location": "/v1/eco/removelocation/",
    # "???": "/v3/eco/myequipmentcheck/", # Unclear how/why used TODO
}


class RheemEcoNet:
    def __init__(self, username, password):
        self._auth = RheemAuth()
        self._auth.start_auth(username, password)

    def getLocations(self):
        requests.get(url, auth=auth)
