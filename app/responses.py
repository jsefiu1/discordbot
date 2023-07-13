import discord
from discord import Embed
import random
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.utils.google_search import search_google
from app.utils.currency import currency_convert
from app.utils.chatGPT import chatGPT_response
from app.utils.commands import help_command, commands_telegrafi, commands_gpt, commands_google, commands_currencies

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
        if p_message_list[1] == "telegrafi":
            await commands_telegrafi(channel, username, is_private)
        elif p_message_list[1] == "gpt":
            await commands_gpt(channel, username, is_private)
        elif p_message_list[1] == "google":
            await commands_google(channel, username, is_private)
        elif p_message_list[1] == "currencies":
            await commands_currencies(channel, username, is_private)
        else:
            return "Please correctly specify the website that you want commands for!"
         
    if p_message_list[0] == "/scrape":
        # TODO: add checks for all cases
        if p_message_list[1] == "telegrafi":
            scrape_result = await scrape_telegrafi(p_message_list, channel, username, is_private)
            return scrape_result
        else:
            return "Incorrect scraper name! Try one of ['telegrafi', 'gjirafa', 'kosovajob']"

    if p_message_list[0] == "/data":
        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel, username, is_private)
        else:
            return "Incorrect table name! Try one of ['telegrafi', 'gjirafa', 'kosovajob']"
        
    if p_message_list[0] == "!google":
        search_result = await search_google(p_message_list, channel, username, is_private)
        return search_result
    
    if p_message_list[0] == "!convert":
        convert_result = await currency_convert(p_message_list, channel, username, is_private)
        return convert_result
    
    if p_message_list[0] == "/gpt":
        gpt_result = await chatGPT_response(p_message_list, channel, username, is_private)
        return gpt_result

