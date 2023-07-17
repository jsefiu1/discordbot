from discord import Embed
import random
import discord
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.api_functions.gjirafa import scrape_gjirafa, data_gjirafa
from app.utils.google_search import search_google
from app.utils.currency import currency_convert
from app.utils.chatGPT import chatGPT_response
from app.utils.weather import process_weather_command
from app.utils.nasa import process_nasa_command
from app.utils.commands import help_command, commands_telegrafi, commands_gpt, commands_google, commands_currencies
from app.utils.commands import commands_gjirafa, commands_weather, commands_nasa



async def handle_response(user_message, channel, username, is_private) -> Embed:
    p_message: str = user_message.lower()
    p_message_list = p_message.split(" ")
    if p_message == "hello":
        return f"Hey there {username}"

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        await help_command(channel, username, is_private)

    if p_message_list[0] == "/commands":
        if len(p_message_list) < 2:
            return "Please specify the API that you want commands for!"
        
        if p_message_list[1] == "telegrafi":
            await commands_telegrafi(channel, username, is_private)
        elif p_message_list[1] == "gpt":
            await commands_gpt(channel, username, is_private)
        elif p_message_list[1] == "google":
            await commands_google(channel, username, is_private)
        elif p_message_list[1] == "currencies":
            await commands_currencies(channel, username, is_private)
        elif p_message_list[1] == "gjirafa":
            await commands_gjirafa(channel, username, is_private)
        elif p_message_list[1] == "weather":
            await commands_weather(channel, username, is_private)
        elif p_message_list[1] == "nasa":
            await commands_nasa(channel, username, is_private)
        else:
            return "Invalid API specified for commands!"

    if p_message_list[0] == "/scrape":
        if len(p_message_list) >= 2:
            if p_message_list[1] == "telegrafi":
                scrape_result = await scrape_telegrafi(p_message_list, channel, is_private)
                return scrape_result
            elif p_message_list[1] == "gjirafa":
                scrape_result = await scrape_gjirafa(p_message_list, channel, username, is_private)
                return scrape_result
        return "Incorrect scraper name! Please scpecify it correctly"

    if p_message_list[0] == "/data":
        if len(p_message_list) < 2:
            return "Please specify the API for data retrieval!"

        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel)

        elif p_message_list[1] == "gjirafa":
            await data_gjirafa(p_message_list, channel, username, is_private)

        else:
            return "Invalid API specified for data retrieval!"

    if p_message_list[0] == "/weather":
        await  process_weather_command(p_message_list, channel,username, is_private)

    if p_message_list[0] == "/nasa":
        await process_nasa_command(p_message_list, channel,username, is_private)

    if p_message_list[0] == "!google":
        search_result = await search_google(p_message_list, channel, username, is_private)
        return search_result
    
    if p_message_list[0] == "!convert":
        convert_result = await currency_convert(p_message_list, channel, username, is_private)
        return convert_result
    
    if p_message_list[0] == "/gpt":
        gpt_result = await chatGPT_response(p_message_list, channel, username, is_private)
        return gpt_result