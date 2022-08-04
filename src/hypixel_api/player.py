from collections import namedtuple

import requests

from hypixel_api.utilities import username_from_UUID

from .exceptions import InvalidUUIDException


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