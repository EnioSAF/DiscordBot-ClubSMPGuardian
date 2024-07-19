import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(message.content)

client.run(TOKEN)
