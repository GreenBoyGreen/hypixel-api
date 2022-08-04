import requests


def username_from_UUID(UUID):
    try:
        return requests.get(f"https://playerdb.co/api/player/minecraft/{UUID}").json()["data"]["player"]["username"]
    except KeyError:
        return "Service currently unreachable"

def UUID_from_username(username):
    try:
        return requests.get(f"https://playerdb.co/api/player/minecraft/{username}").json()["data"]["player"]["id"]
    except KeyError:
        return "Service currently unreachable"