import requests

def get_achievements():
    return requests.get("https://api.hypixel.net/resources/achievements").json()

def get_guild_achievements():
    return requests.get("https://api.hypixel.net/resources/guilds/achievements").json()

def get_challenges():
    return requests.get("https://api.hypixel.net/resources/challenges").json()

def get_quests():
    return requests.get("https://api.hypixel.net/resources/quests").json()

def get_vanity_pets():
    return requests.get("https://api.hypixel.net/resources/vanity/pets").json()

def get_vanity_companions():
    return requests.get("https://api.hypixel.net/resources/vanity/companions").json()