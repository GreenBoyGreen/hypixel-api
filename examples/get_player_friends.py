import hypixel_api
from hypixel_api.utilities import UUID_from_username

api_key = "your_key"
player_name = "username"


connection = hypixel_api.Hypixel(api_key)
owner = connection.owner
print(f"Authenticated as {owner.username} ({owner.UUID}) with the key {connection.key}")
player = hypixel_api.Player(UUID_from_username(player_name))
player.get_data(connection)
friends, uuids = player.get_friends()
for i in friends:
    print(i)