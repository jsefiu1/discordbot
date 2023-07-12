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
        await ctx.send(formatted_data)
    else:
        await ctx.send("Unable to fetch weather data. Please try again later.")


def format_weather_data(weather_data):
    name = weather_data["name"]
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    
    message = f"Weather in {name}\n\n"
    message += f"Description: {weather_desc}\n"
    message += f"Temperature: {temp}°C\n"
    message += f"Humidity: {humidity}%"
    
    return message
