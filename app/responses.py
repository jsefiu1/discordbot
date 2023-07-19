from discord import Embed
import random
import discord
from discord import Embed
from io import BytesIO
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.api_functions.ofertasuksesi import scrape_ofertasuksesi, data_ofertasuksesi
from app.api_functions.gjirafa import data_gjirafa, scrape_gjirafa
from app.utils.unsplash import generate_image
from app.utils.youtube import search_youtube_videos
from app.utils.quotes import generate_quote
from app.utils.jokes import generate_joke
from app.utils.dictionary import search_word_definition
from app.utils.movie import get_movie_info
from app.utils.crypto import get_crypto_info
from app.utils.google_search import search_google
from app.utils.currency import currency_convert
from app.utils.chatGPT import chatGPT_response
from app.utils.weather import process_weather_command
from app.utils.nasa import process_nasa_command
from app.utils.commands import help_command, commands_telegrafi, commands_gpt, commands_google, commands_currencies
from app.utils.commands import commands_gjirafa, commands_weather, commands_nasa
from app.utils.commands import commands_ofertasuksesi, crypto_commands


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
        elif p_message_list[1] == "ofertasuksesi":
            await commands_ofertasuksesi(channel, username, is_private)
        elif p_message_list[1] == "crypto":
            await crypto_commands(channel, username, is_private)
            
        else:
            return "Invalid API specified for commands!"

    if p_message_list[0] == "/scrape":
        if len(p_message_list) >= 2:
            if p_message_list[1] == "telegrafi":
                scrape_result = await scrape_telegrafi(p_message_list, channel, username, is_private)
                return scrape_result
            elif p_message_list[1] == "gjirafa":
                scrape_result = await scrape_gjirafa(p_message_list, channel, username, is_private)
                return scrape_result
            elif p_message_list[1] == "ofertasuksesi":
                scrape_result = await scrape_ofertasuksesi(p_message_list, channel, username, is_private)
                return scrape_result

        else:
            return "Incorrect scraper name! Please scpecify it correctly"

    if p_message_list[0] == "/data":
        if len(p_message_list) < 2:
            return "Please specify the API for data retrieval!"

        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel, username, is_private)

        elif p_message_list[1] == "gjirafa":
            await data_gjirafa(p_message_list, channel, username, is_private)

        elif p_message_list[1] == "ofertasuksesi":
            data = await data_ofertasuksesi(p_message_list, channel, username, is_private)
            return data

        else:
            return "Incorrect table name! Try one of ['telegrafi', 'kosovajobs', 'ofertasuksesi']"

    if p_message_list[0] == "/img":
        if p_message_list[1]:
            await generate_image(p_message_list[1], channel, username, is_private)
        
    if p_message_list[0] == "/youtube":
        await search_youtube_videos(p_message_list[1], username, channel, is_private)
    
    if p_message_list[0] == "/quote":
       await generate_quote(username, channel, is_private)

    if p_message_list[0] == "/joke":
       await generate_joke(is_private, username, channel)

    if p_message_list[0] == "/define":
        word = ' '.join(p_message_list[1:])
        definition = await search_word_definition(word, channel, username, is_private)
        return definition
        # if is_private:
        #     await username.send(definition)
        # else:
        #     await channel.send(definition)
    
    if p_message_list[0] == "/movie":
        await get_movie_info(p_message_list[1], username, channel, is_private)

    if p_message_list[0] == "/crypto":
        await get_crypto_info(p_message_list[1], username, channel, is_private)