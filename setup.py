import os

def create_env_file():
    # Collecting necessary information
    discord_bot_token = input("Enter your Discord Bot Token: ")
    guild_id = input("Enter your Discord Guild ID: ")
    twitch_client_id = input("Enter your Twitch Client ID: ")
    twitch_client_secret = input("Enter your Twitch Client Secret: ")
    twitch_access_token = input("Enter your Twitch Access Token: ")
    twitch_usernames = input("Enter the Twitch Usernames (comma separated): ")
    discord_channel_id = input("Enter the Discord Channel ID for notifications: ")

    # Creating .env file
    with open(".env", "w") as env_file:
        env_file.write(f"DISCORD_BOT_TOKEN={discord_bot_token}\n")
        env_file.write(f"GUILD_ID={guild_id}\n")
        env_file.write(f"TWITCH_CLIENT_ID={twitch_client_id}\n")
        env_file.write(f"TWITCH_CLIENT_SECRET={twitch_client_secret}\n")
        env_file.write(f"TWITCH_ACCESS_TOKEN={twitch_access_token}\n")
        env_file.write(f"TWITCH_USERNAMES={twitch_usernames}\n")
        env_file.write(f"DISCORD_CHANNEL_ID={discord_channel_id}\n")

    print(".env file created successfully.")

def install_dependencies():
    # Install necessary dependencies
    os.system("pip install -r requirements.txt")

if __name__ == "__main__":
    create_env_file()
    install_dependencies()