import random
import discord
from discord import Embed
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.api_functions.gjirafa import scrape_gjirafa, data_gjirafa, create_gjirafa_embed, process_gjirafa_command
from app.utils.weather import get_weather, format_weather_data, process_weather_command
from app.utils.nasa import get_nasa_apod, format_nasa_apod, process_nasa_command
from app.utils.commands import commands_gjirafa, commands_weather, commands_nasa

async def handle_response(user_message, channel, username) -> str:
    p_message: str = user_message.lower()
    p_message_list = p_message.split(" ")

    if p_message == "hello":
        return f"Hey there {username}"

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "This is a help message"

    if p_message_list[0] == "/commands":
        if p_message_list[1] == "gjirafa":
            await commands_gjirafa(channel, username)
        elif p_message_list[1] == "weather":
            await commands_weather(channel, username)
        elif p_message_list[1] == "nasa":
            await commands_nasa(channel, username)    
        else:
            return "Please correctly specify the API that you want commands for!"

    if p_message_list[0] == "/scrape":
        if len(p_message_list) >= 2:
            if p_message_list[1] == "telegrafi":
                scrape_result = await scrape_telegrafi(p_message_list, channel)
                return scrape_result

            if p_message_list[1] == "gjirafa":
                scrape_result = await scrape_gjirafa(p_message_list, channel)
                return scrape_result

    if p_message_list[0] == "/data":
        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel)
            return None

        if p_message_list[1] == "gjirafa":
            result = await process_gjirafa_command(p_message_list, channel)
            if isinstance(result,discord.Embed):
                await channel.send(embed=result)
            else:
                await channel.send(result)
            return None

    if p_message_list[0] == "/weather":
        result = await process_weather_command(p_message_list, channel)
        if isinstance(result, discord.Embed):
            await channel.send(embed=result)
        else:
            await channel.send(result)
        return None

    if p_message_list[0] == "/nasa":
        result = await process_nasa_command(p_message_list, channel)
        if isinstance(result, discord.Embed):
            await channel.send(embed=result)
        else:
            await channel.send(result)
        return None 

        return "Invalid command."