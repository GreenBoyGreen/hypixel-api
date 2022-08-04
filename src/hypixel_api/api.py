import requests

from .exceptions import InvalidApiKeyException, RequestLimitReachedException
from .player import Player


class Api:
    def __init__(self, key):
        self.key = key
        key_info = self.test_key()["record"]
        self.owner = Player(key_info["owner"])
        self.limit = key_info["limit"]
        self.queriesInPastMin = key_info["queriesInPastMin"]
        self.totalQueries = key_info["totalQueries"]

    def test_key(self):
        key_test_request = requests.get(f"https://api.hypixel.net/key?key={self.key}")
        match key_test_request.status_code:
            case 200:
                return key_test_request.json()
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")

    def login_message(self):
        print(f"Logged in as {self.owner.username} ({self.owner.uuid}) with \"{self.key}\"")
