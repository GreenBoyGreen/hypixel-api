import datetime
from tokenize import String
import requests
import re

from hypixel_api.utilities import username_from_UUID

from .exceptions import InvalidApiKeyException, InvalidUUIDException, RequestLimitReachedException, UnknownPLayerException


class Player:
    def __init__(self, UUID=String):
        self.UUID = UUID.replace("-", "")
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
        friends_request = requests.get(f"https://api.hypixel.net/friends?key={hypixel.key}&uuid={self.UUID}")
        match friends_request.status_code:
            case 200:
                self.friends = friends_request.json()["records"]
            case 403:
                raise InvalidApiKeyException("Invalid API Key")
            case 429:
                raise RequestLimitReachedException("Request Limit Reached")
    

    def set_data(self, request_json):
        if request_json == None:
            raise UnknownPLayerException("Unknown Player")
        try:
            self.language = request_json["userLanguage"]
        except:
            self.language = None
        self.rank = self.get_rank(request_json)
        try:
            self.first_login = datetime.datetime.fromtimestamp(request_json["first_login"] / 1000)
        except Exception:
            self.first_login = None
        try:
            self.last_login = datetime.datetime.fromtimestamp(request_json["lastLogin"] / 1000)
        except Exception:
            self.last_login = None
        try:
            self.last_logout = datetime.datetime.fromtimestamp(request_json["lastLogout"] / 1000)
        except Exception:
            self.last_logout = None
        try:
            self.one_time_achievements = request_json["achievementsOneTime"]
        except Exception:
            self.one_time_achievements = None
        try:
            social_media = request_json["socialMedia"]["links"]
        except Exception:
            social_media = None
        try:
            self.discord = social_media["DISCORD"]
        except Exception:
            self.discord = None
        try:
            self.twitter = social_media["TWITTER"]
        except Exception:
            self.twitter = None
        try:
            self.youtube = social_media["YOUTUBE"]
        except Exception:
            self.youtube = None
        try:
            self.instagram = social_media["INSTAGRAM"]
        except Exception:
            self.instagram = None
        try:
            self.twitch = social_media["TWITCH"]
        except Exception:
            self.twitch = None
        try:
            self.hypixel = social_media["HYPIXEL"]
        except Exception:
            self.hypixel = None


    def get_rank(self, request_json):
        if "prefix" in request_json:
            return re.sub("§.", "", request_json["prefix"])
        elif "rank" in request_json:
            match request_json["rank"]:
                case "ADMIN":
                    return "[ADMIN]"
                case "GAME_MASTER":
                    return "[GM]"
                case "MODERATOR":
                    return "[MOD]"
                case "YOUTUBER":
                    return "[YOUTUBE]"
                case "NORMAL":
                    return ""
                case _:
                    return request_json["rank"]
        elif "monthlyPackageRank" in request_json:
            return "[MVP++]"
        elif "newPackageRank" in request_json:
            match request_json["newPackageRank"]:
                case "VIP":
                    return "[VIP]"
                case "VIP_PLUS":
                    return "[VIP+]"
                case "MVP":
                    return "[MVP]"
                case "MVP_PLUS":
                    return "[MVP+]"
        elif "PackageRank" in request_json:
            match request_json["PackageRank"]:
                case "VIP":
                    return "[VIP]"
                case "VIP_PLUS":
                    return "[VIP+]"
                case "MVP":
                    return "[MVP]"
                case "MVP_PLUS":
                    return "[MVP+]"
        else:
            return ""


    def get_friends(self):
        friends = list()
        friends_uuid = list()
        for i in self.friends:
            if i["uuidSender"] == self.UUID:
                friends.append(username_from_UUID(i['uuidReceiver']))
                friends_uuid.append({i['uuidReceiver']})
            else:
                friends.append(username_from_UUID(i['uuidSender']))
                friends_uuid.append({i['uuidSender']})
        return friends, friends_uuid