import random
import discord
from discord import Embed
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.api_functions.gjirafa import scrape_gjirafa, data_gjirafa, create_gjirafa_embed
from app.utils.weather import get_weather, format_weather_data
from app.utils.nasa import get_nasa_apod, format_nasa_apod

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
            with open("app/text-files/commands_gjirafa.txt", "r") as file:
                content = file.read()
                embed = Embed(title="Gjirafa Commands", description=content, color=discord.Color.green())
                if isinstance(channel, discord.DMChannel):
                    await username.send(embed=embed)
                else:
                    await channel.send(embed=embed)
            return None

        if p_message_list[1] == "weather":
            with open("app/text-files/commands_weather.txt", "r") as file:
                content = file.read()
                embed = Embed(title="Weather Command", description=content, color=discord.Color.green())
                if isinstance(channel, discord.DMChannel):
                    await username.send(embed=embed)
                else:
                    await channel.send(embed=embed)
            return None

        if p_message_list[1] == "nasa":
            with open("app/text-files/commands_nasa.txt", "r") as file:
                content = file.read()
                embed = Embed(title="Nasa Command", description=content, color=discord.Color.green())
                if isinstance(channel, discord.DMChannel):
                    await username.send(embed=embed)
                else:
                    await channel.send(embed=embed)
            return None

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
            if len(p_message_list) >= 3:
                query_params = {}
                for arg in p_message_list[2:]:
                    if ":" in arg:
                        key, value = arg.split(":")
                        query_params[key] = value
                results = await data_gjirafa(p_message_list, channel)
                return results
            else:
                return "Invalid arguments for Gjirafa data retrieval. Use 'name:value' format."

    if p_message_list[0] == "/weather":
        if len(p_message_list) >= 2:
            location = p_message_list[1]
            weather_data = get_weather(location)
            if weather_data:
                formatted_data = format_weather_data(weather_data)
                return formatted_data
            else:
                return "Unable to fetch weather data. Please try again later."
        else:
            return "Please provide a location for the weather command." 

    if p_message_list[0] == "/nasa":
        if len(p_message_list) >= 2:
            if p_message_list[1] == "random":
                apod_data = get_nasa_apod(1)  
                if apod_data:
                    random_apod = apod_data[0]
                    embed = format_nasa_apod([random_apod])
                    return embed
                else:
                    return "Unable to fetch APOD data. Please try again later."
            else:
                query = " ".join(p_message_list[1:])
                apod_data = get_nasa_apod(10)  
                if apod_data:
                    filtered_data = [
                        item for item in apod_data
                        if query.lower() in item.get("title", "").lower()
                        or query.lower() in item.get("explanation", "").lower()
                    ]
                    if filtered_data:
                        embed = format_nasa_apod(filtered_data)
                        return embed
                    else:
                        return f"No APOD found related to '{query}'."
                else:
                    return "Unable to fetch APOD data. Please try again later."
        else:
            return "Please provide a command or query for the NASA command."

    return "Invalid command."
