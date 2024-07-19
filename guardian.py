import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN') # BOT TOKE
GUILD_ID = os.getenv('GUILD_ID') # DISCORD SERVER ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot made by Enio SadFlower for the ClubSMP Discord Server.')
    print(f'Connecté en tant que {bot.user}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
        print(f'Synchronisé {len(synced)} commandes')
    except Exception as e:
        print(f'Erreur lors de la synchronisation: {e}')

@bot.tree.command(name='say', description='Répète le message spécifié', guild=discord.Object(id=int(GUILD_ID)))
@app_commands.checks.has_permissions(administrator=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@say.error
async def say_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)

bot.run(TOKEN)
