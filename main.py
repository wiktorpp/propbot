import discord
from TOKENS import inventory as inventory_token
from TOKENS import phone as phone_token
from TOKENS import surroundings as surroundings_token
from TOKENS import vacuum as vacuum_token

import asyncio
from mansion import id_to_room_name, room_name_to_id
#from characters import id_to_character_name

class clients:
    inventory = discord.Client()
    phone = discord.Client()
    surroundings = discord.Client()
    vacuum = discord.Client()

@clients.inventory.event
async def on_ready(): print(f"\033[31mLogged in as {clients.inventory.user} (inventory)\033[39m")

@clients.phone.event
async def on_ready(): print(f"\033[31mLogged in as {clients.phone.user} (phone)\033[39m")

class off: pass

class Character:
    def __init__(self, id, name, member=None, in_room_id=None):
        self.id = id
        self.name = name
        self.member = member
        self.room_id = in_room_id
        self.in_a_call_with = None
        self.is_being_called_by = None
    
    def __repr__(self) -> str:
        return f"Character({self.id}, {self.name}, in_room_id={self.in_room.id})"
    
    def __str__(self) -> str:
        return self.name

    def get_room(self):
        #get channel by id
        channel = clients.phone.get_channel(self.room_id)
        return channel

character_name_to_character_object = {
    "Roomba": Character(496709767914586112, "Roomba", in_room_id=967113761808859269),
    "Theo": Character(687974477312557097, "Theo", in_room_id=967113761808859269),
    "Paddy": Character(718094142428676126, "Paddy", in_room_id=971367884766998598),
}

id_to_character_name = {}
for character in character_name_to_character_object.values():
    id_to_character_name[character.id] = character.name

async def send_message_as(client, channel_id, message):
    #get channel
    channel = client.get_channel(channel_id)
    #send message
    await channel.send(message)

async def react_thumbs_up(message):
    await message.add_reaction("👍")

async def message_invalid(message):
    #delete an invalid message
    await message.delete()

@clients.phone.event
async def on_message(message):
    if message.author == clients.phone.user:
        return

    self_character = character_name_to_character_object[id_to_character_name[message.author.id]]

    print(character)

    if self_character.member is None:
        self_character.member = message.author
    
    if message.content.startswith("!dump_characters"):
        await message.channel.send(str(character_name_to_character_object))

    if (not self_character.in_a_call_with is None) and (not self_character.in_a_call_with is off):
        callee = character_name_to_character_object[self_character.in_a_call_with]
        await callee.get_room().send(f"{self_character}> {message.content}")

    if ".calls" in message.content:
        other_character_name = message.content.split(".calls")[1].strip().strip("*")
        other_character = character_name_to_character_object[other_character_name]
        await react_thumbs_up(message)
        if other_character.in_a_call_with is None and other_character.is_being_called_by is None:
            other_character.is_being_called_by = self_character
            await other_character.get_room().send(
                f"{self_character} is calling you!\n"
                f"||(Use *.answers* or *.hangs up*)||"
            )
        else:
            await message.channel.send(f"*busy signal*")

    if ".answers" in message.content:
        other_character = self_character.is_being_called_by
        other_character.in_a_call_with = self_character.name
        self_character.in_a_call_with = other_character.name
    
    if ".hangs up" in message.content:
        other_character = self_character.is_being_called_by
        other_character.get_room().send(f"{self_character} has hung up.")
        self_character.is_being_called_by = None

    if ".turns off" in message.content:
        if self_character.in_a_call_with is None:
            self_character.in_a_call_with = off
            await react_thumbs_up(message)
        else:
            await message_invalid(message)
    
    if ".turns on" in message.content:
        if self_character.in_a_call_with is off:
            self_character.in_a_call_with = None
            await react_thumbs_up(message)
        else:
            await message_invalid(message)
    
    if ".enters" in message.content:
        room = message.channel
        self_character.room_id = room.id
        await message.channel.send(f"{self_character} enters {room}")

    print(message.content)
    

        
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(clients.inventory.start(inventory_token))
    loop.create_task(clients.phone.start(phone_token))
    #loop.create_task(client.surroundings.start(surroundings_token))
    loop.run_forever()