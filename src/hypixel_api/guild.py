import datetime
import re
import requests

from hypixel_api.exceptions import InvalidApiKeyException, RequestLimitReachedException
from hypixel_api.player import Player


class Guild:
    def __init__(self, hypixel):
        self.hypixel = hypixel

    def set_guild_by_id(self, guild_id):
        guild_request = requests.get(f"https://api.hypixel.net/guild?key={self.hypixel.key}&id={guild_id}")
        match guild_request.status_code:
            case 200:
                self.set_data(guild_request.json()["guild"])
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")

    def set_guild_by_player(self, player=Player):
        guild_request = requests.get(f"https://api.hypixel.net/guild?key={self.hypixel.key}&player={player.UUID}")
        match guild_request.status_code:
            case 200:
                self.set_data(guild_request.json()["guild"])
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")

    def set_guild_by_name(self, name):
        guild_request = requests.get(f"https://api.hypixel.net/guild?key={self.hypixel.key}&name={name}")
        match guild_request.status_code:
            case 200:
                self.set_data(guild_request.json()["guild"])
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")

    def set_data(self, request_json):
        self.name = request_json["name"]
        self.coins = request_json["coins"]
        self.total_coins = request_json["coinsEver"]
        self.members = request_json["members"]
        self.tag = request_json["tag"]
        self.tag_clean = re.sub("§.", "", request_json["tag"])
        self.ranks = request_json["ranks"]
        self.preferred_games = request_json["preferredGames"]
        self.exp_by_game = request_json["guildExpByGameType"]
        self.creation_date = datetime.datetime.fromtimestamp(request_json["created"] / 1000)
        self.id = request_json["_id"]