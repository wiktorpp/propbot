import discord
from TOKENS import inventory as inventory_token
from TOKENS import phone as phone_token
from TOKENS import surroundings as surroundings_token
from TOKENS import vacuum as vacuum_token

import asyncio

class clients:
    inventory = discord.Client()
    phone = discord.Client()
    surroundings = discord.Client()
    vacuum = discord.Client()

@clients.inventory.event
async def on_ready(): print(f"\033[31mLogged in as {clients.inventory.user} (inventory)\033[39m")

@clients.phone.event
async def on_ready(): print(f"\033[31mLogged in as {clients.phone.user} (phone)\033[39m")

@clients.phone.event
async def on_message(message):
    if message.author == clients.phone.user:
        return

    print(message.content)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(clients.inventory.start(inventory_token))
    loop.create_task(clients.phone.start(phone_token))
    #loop.create_task(client.surroundings.start(surroundings_token))
    loop.run_forever()