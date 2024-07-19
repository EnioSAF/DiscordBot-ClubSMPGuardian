import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Load Twitch usernames from a file
TWITCH_USERNAMES_FILE = 'twitch_usernames.json'

def load_twitch_usernames():
    if os.path.exists(TWITCH_USERNAMES_FILE):
        with open(TWITCH_USERNAMES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_twitch_usernames(usernames):
    with open(TWITCH_USERNAMES_FILE, 'w') as f:
        json.dump(usernames, f)

TWITCH_USERNAMES = load_twitch_usernames()

# Dictionary to keep track of live status and message IDs
live_status = {username: False for username in TWITCH_USERNAMES}
live_messages = {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to get a new Twitch access token
def get_new_twitch_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    data = response.json()

    if 'access_token' in data:
        return data['access_token']
    else:
        return None

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print('Bot made by Enio SadFlower for the ClubSMP Discord Server.')
    print(f'Connected as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
    except Exception as e:
        pass

    # Start Twitch live notification task
    check_twitch_streams.start()

# Command: say (admin only)
@bot.tree.command(name='say', description='Repeats the specified message', guild=discord.Object(id=int(GUILD_ID)))
@app_commands.checks.has_permissions(administrator=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@say.error
async def say_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

# Command: list_channels (admin only)
@bot.tree.command(name='list_channels', description='Lists the monitored Twitch channels', guild=discord.Object(id=int(GUILD_ID)))
@app_commands.checks.has_permissions(administrator=True)
async def list_channels(interaction: discord.Interaction):
    await interaction.response.send_message(f"Monitored Twitch channels: {', '.join(TWITCH_USERNAMES)}")

# Command: add_channel (admin only)
@bot.tree.command(name='add_channel', description='Adds a new Twitch channel to monitor', guild=discord.Object(id=int(GUILD_ID)))
@app_commands.checks.has_permissions(administrator=True)
async def add_channel(interaction: discord.Interaction, channel: str):
    if channel not in TWITCH_USERNAMES:
        TWITCH_USERNAMES.append(channel)
        live_status[channel] = False
        save_twitch_usernames(TWITCH_USERNAMES)
        await interaction.response.send_message(f"Channel '{channel}' added to the monitored list.")
    else:
        await interaction.response.send_message(f"Channel '{channel}' is already in the monitored list.")

# Command: remove_channel (admin only)
@bot.tree.command(name='remove_channel', description='Removes a Twitch channel from monitoring', guild=discord.Object(id=int(GUILD_ID)))
@app_commands.checks.has_permissions(administrator=True)
async def remove_channel(interaction: discord.Interaction, channel: str):
    if channel in TWITCH_USERNAMES:
        TWITCH_USERNAMES.remove(channel)
        live_status.pop(channel, None)
        live_messages.pop(channel, None)
        save_twitch_usernames(TWITCH_USERNAMES)
        await interaction.response.send_message(f"Channel '{channel}' removed from the monitored list.")
    else:
        await interaction.response.send_message(f"Channel '{channel}' is not in the monitored list.")

# Background task to check Twitch streams
@tasks.loop(minutes=1)
async def check_twitch_streams():
    global TWITCH_ACCESS_TOKEN
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_ACCESS_TOKEN}'
    }

    for username in TWITCH_USERNAMES:
        params = {'user_login': username}
        url = 'https://api.twitch.tv/helix/streams'
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 401:  # Unauthorized
            new_token = get_new_twitch_token()
            if new_token:
                TWITCH_ACCESS_TOKEN = new_token
                headers['Authorization'] = f'Bearer {TWITCH_ACCESS_TOKEN}'
                response = requests.get(url, headers=headers, params=params)
            else:
                continue

        data = response.json()

        if 'data' in data and data['data']:
            if not live_status[username]:
                live_status[username] = True
                stream = data['data'][0]
                title = stream['title']
                viewers = stream['viewer_count']
                stream_url = f'https://www.twitch.tv/{username}'

                channel = bot.get_channel(DISCORD_CHANNEL_ID)
                message = await channel.send(f"{username} is now live: {title} - {viewers} viewers\n{stream_url}")
                live_messages[username] = message.id
        else:
            if live_status[username]:
                live_status[username] = False
                channel = bot.get_channel(DISCORD_CHANNEL_ID)
                if username in live_messages:
                    message = await channel.fetch_message(live_messages[username])
                    await message.delete()
                    live_messages.pop(username, None)

# Error handling for the Twitch task
@check_twitch_streams.error
async def on_check_twitch_streams_error(error):
    pass

# Run the bot
bot.run(TOKEN)
