import discord
from app import responses
from discord import Intents

gjirafa_channel_id = 1127939891603452005
weather_channel_id = 1127939921802448936

async def send_message(message, user_message, is_private, target_channel):
    try:
        response = await responses.handle_response(user_message, message.channel, message.author)
        await target_channel.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = "MTEyNTg5MjkwMzYwOTMxOTQ2Ng.GLZNuR.CQQxuTMuSS_az3SfnNtVNVvNSsIesguASZbu3Q"
    intents = Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True, target_channel=None)
        elif user_message.startswith("/weather"):
            if message.channel.id == weather_channel_id:
                weather_channel = client.get_channel(weather_channel_id)
                await send_message(message, user_message, is_private=False, target_channel=weather_channel)
            else:
                await message.channel.send("The /weather command is not allowed in this channel.")
        elif user_message.startswith("/gjirafa"):
            if message.channel.id == gjirafa_channel_id:
                gjirafa_channel = client.get_channel(gjirafa_channel_id)
                if len(user_message.split()) >= 2:
                    await send_message(message, user_message, is_private=False, target_channel=gjirafa_channel)
                else:
                    await gjirafa_channel.send("Invalid arguments for Gjirafa scraping. Use 'name:value' format.")
            else:
                await message.channel.send("The /gjirafa command is not allowed in this channel.")
        else:
            await send_message(message, user_message, is_private=False, target_channel=None)


    client.run(TOKEN)
