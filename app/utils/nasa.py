import requests
import discord

API_KEY = "8wUgXmiNbUPEprFLFV5iomC68uESxv440NcBlxKw"
BASE_URL = "https://api.nasa.gov/planetary/apod"

def get_nasa_apod(num_days):
    url = f"{BASE_URL}?api_key={API_KEY}&count={num_days}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def get_random_apod():
    url = f"{BASE_URL}?api_key={API_KEY}&count=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()[0]
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def format_nasa_apod(apod_data):
    embed = discord.Embed(title="NASA Astronomy Picture of the Day", color=discord.Color.blue())

    if len(apod_data) > 0:
        
        item = apod_data[0]

        title = item.get("title", "")
        explanation = item.get("explanation", "")
        image_url = item.get("url", "")

        truncated_title = title[:256] + "..." if len(title) > 256 else title
        truncated_explanation = explanation[:512] + "..." if len(explanation) > 512 else explanation

        embed.add_field(name="Title", value=truncated_title, inline=False)
        embed.add_field(name="Explanation", value=truncated_explanation, inline=False)
        embed.set_image(url=image_url)
        embed.add_field(name="\u200b", value="\u200b", inline=False)  

    return embed
