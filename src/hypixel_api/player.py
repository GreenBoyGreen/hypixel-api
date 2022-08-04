from collections import namedtuple
import datetime

import requests

from hypixel_api.utilities import username_from_UUID

from .exceptions import InvalidApiKeyException, InvalidUUIDException, RequestLimitReachedException


class Player:
    def __init__(self, UUID):
        self.UUID = UUID
        self.test_UUID()
        self.username = username_from_UUID(self.UUID)

    def test_UUID(self):
        uuid_test_request = requests.get(f"https://playerdb.co/api/player/minecraft/{self.UUID}")
        match uuid_test_request.status_code:
            case 200:
                return uuid_test_request.json()
            case 403:
                raise InvalidUUIDException("Invalid UUID")

    def get_data(self, hypixel):
        data_request = requests.get(f"https://api.hypixel.net/player?key={hypixel.key}&uuid={self.UUID}")
        match data_request.status_code:
            case 200:
                self.set_data(data_request.json()["player"])
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")
    
    def set_data(self, request_json):
        self.first_login = datetime.datetime.fromtimestamp(request_json["firstLogin"] / 1000)
        self.last_login = datetime.datetime.fromtimestamp(request_json["lastLogin"] / 1000)
