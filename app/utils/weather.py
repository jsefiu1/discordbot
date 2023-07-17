import discord
import requests

API_KEY = "0647cac0ee3b6c7d07cc06bb722e34c7"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def process_weather_command(p_message_list, channel,username, is_private):
  
    if isinstance(channel, discord.DMChannel):
        weather_channel = channel
    else:
        weather_channel = discord.utils.get(channel.guild.channels, name="weather")

    if weather_channel is not None or channel.permissions_for(username).administrator:

       
        location = p_message_list[1] if len(p_message_list) >= 2 else None

        if location:
            params = {
                "q": location,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                weather_data = response.json()

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
                embed.add_field(name="Temperature (Fahrenheit)", value=f"{temp_fahrenheit}°F", inline=True)

                result = embed

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                result = "Unable to fetch weather data. Please try again later."

        else:
            result = "Please provide a location for the weather command."

        if is_private:
            await username.send(embed=embed)
        else:
            await weather_channel.send(embed=embed)
    else:
        await channel.send("This command only will work in channel weather or private")