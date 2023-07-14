import discord
from app import responses
from discord import Intents


async def send_message(message, user_message, is_private):
    try:
        response = await responses.handle_response(
            user_message, message.channel, message.author, is_private
        )
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = "MTEyNzM4NTI5NTcwOTU1Njc1Ng.GMC8x-.UAxwELWpLMibGmUBQoHopoYJ5Em4AgR9n9UFH0"
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
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
