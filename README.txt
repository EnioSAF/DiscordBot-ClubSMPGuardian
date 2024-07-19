
# ClubSMP Guardian Discord Bot

## Overview

ClubSMP Guardian is a Discord bot designed for the ClubSMP Discord server. It has various functionalities including sending notifications when specified Twitch channels go live.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

git clone https://github.com/yourusername/ClubSMP-Guardian.git
cd ClubSMP-Guardian


### Step 2: Run the Setup Script

Run the setup script to create the `.env` file and install necessary dependencies:

python setup.py


The setup script will prompt you to enter the following information:

1. **Discord Bot Token**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application.
   - Under the "Bot" section, click "Add Bot" and then "Copy" the token.

2. **Discord Guild ID**:
   - Open Discord and go to your server.
   - Right-click on the server name and click "Copy ID". (You need to enable Developer Mode in Discord settings to see this option)

3. **Twitch Client ID and Client Secret**:
   - Go to the [Twitch Developer Console](https://dev.twitch.tv/console/apps).
   - Create a new application.
   - You will get the Client ID and Client Secret.

4. **Twitch Access Token**:
   - Use [Twitch Token Generator](https://twitchtokengenerator.com/) to generate an access token. Make sure to set the redirect URL in your Twitch application settings to `https://twitchtokengenerator.com`.

5. **Twitch Usernames**:
   - Enter the Twitch usernames you want to monitor, separated by commas.

6. **Discord Channel ID**:
   - Open Discord and go to the channel where you want to send notifications.
   - Right-click on the channel name and click "Copy ID". (You need to enable Developer Mode in Discord settings to see this option)

### Step 3: Run the Bot

After running the setup script and creating the `.env` file, you can start the bot with:

python guardian.py


## .env File Example

Here is an example of what your `.env` file should look like:


DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
GUILD_ID=YOUR_GUILD_ID
TWITCH_CLIENT_ID=YOUR_TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET=YOUR_TWITCH_CLIENT_SECRET
TWITCH_ACCESS_TOKEN=YOUR_TWITCH_ACCESS_TOKEN
TWITCH_USERNAMES=twitchusername1,twitchusername2
DISCORD_CHANNEL_ID=YOUR_DISCORD_CHANNEL_ID


## Dependencies

The necessary dependencies are listed in the `requirements.txt` file. They will be installed automatically when you run the setup script. The dependencies are:
- discord.py
- python-dotenv
- requests

## Troubleshooting

If you encounter any issues, make sure:
- All tokens and IDs are correctly entered in the `.env` file.
- Your bot has the necessary permissions in your Discord server.
- You have correctly set the redirect URL in your Twitch application settings.

For further assistance, refer to the documentation of the libraries used or contact the repository maintainer.
