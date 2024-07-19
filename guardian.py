import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
TWITCH_USERNAMES = os.getenv('TWITCH_USERNAMES').lower().split(',')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

print(f"Discord Bot Token: {TOKEN}")
print(f"Guild ID: {GUILD_ID}")
print(f"Twitch Client ID: {TWITCH_CLIENT_ID}")
print(f"Twitch Client Secret: {TWITCH_CLIENT_SECRET}")
print(f"Twitch Access Token: {TWITCH_ACCESS_TOKEN}")
print(f"Twitch Usernames: {TWITCH_USERNAMES}")
print(f"Discord Channel ID: {DISCORD_CHANNEL_ID}")

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

    print(f"Token request response: {data}")

    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"Failed to get a new token: {data}")
        return None

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print('Bot made by Enio SadFlower for the ClubSMP Discord Server.')
    print(f'Connected as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
        print(f'Synchronized {len(synced)} commands')
    except Exception as e:
        print(f'Error during synchronization: {e}')

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

# Background task to check Twitch streams
@tasks.loop(minutes=5)
async def check_twitch_streams():
    global TWITCH_ACCESS_TOKEN
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_ACCESS_TOKEN}'
    }

    for username in TWITCH_USERNAMES:
        params = {'user_login': username}
        url = 'https://api.twitch.tv/helix/streams'
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Params: {params}")

        response = requests.get(url, headers=headers, params=params)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")

        if response.status_code == 401:  # Unauthorized
            print("Access token expired, fetching a new one...")
            new_token = get_new_twitch_token()
            if new_token:
                TWITCH_ACCESS_TOKEN = new_token
                headers['Authorization'] = f'Bearer {TWITCH_ACCESS_TOKEN}'
                response = requests.get(url, headers=headers, params=params)
                print(f"New response status code: {response.status_code}")
                print(f"New response headers: {response.headers}")
            else:
                print("Failed to renew access token")
                continue

        data = response.json()
        print(f"Response from Twitch API for {username}: {data}")

        if 'data' in data and data['data']:
            stream = data['data'][0]
            title = stream['title']
            viewers = stream['viewer_count']
            stream_url = f'https://www.twitch.tv/{username}'

            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(f"{username} is now live: {title} - {viewers} viewers\n{stream_url}")
        else:
            print(f"No live stream found for {username}")

# Error handling for the Twitch task
@check_twitch_streams.error
async def on_check_twitch_streams_error(error):
    print(f'Error checking Twitch streams: {error}')

# Run the bot
bot.run(TOKEN)