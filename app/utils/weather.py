import discord
import requests

API_KEY = "0647cac0ee3b6c7d07cc06bb722e34c7"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(location):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

async def display_weather(ctx, location):
    weather_data = get_weather(location)
    if weather_data:
        formatted_data = format_weather_data(weather_data)
        await ctx.send(embed=formatted_data)
    else:
        await ctx.send("Unable to fetch weather data. Please try again later.")

def format_weather_data(weather_data):
    embed = discord.Embed(title="Weather data", color=discord.Color.blue())

    name = weather_data["name"]
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    temp_fahrenheit = (temp * 9/5) + 32
    temp_fahrenheit = round(temp_fahrenheit, 3)
    humidity = weather_data["main"]["humidity"]

    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Description", value=weather_desc, inline=True)
    embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
    embed.add_field(name="Temperature (Celsius)", value=f"{temp}°C", inline=False)
    embed.add_field(name="Temperature (Fahrenheit)", value=f'{temp_fahrenheit}°F', inline=True)

    return embed

async def process_weather_command(p_message_list, channel):
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