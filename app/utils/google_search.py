import discord
from discord import Embed
from googleapiclient.discovery import build

API_KEY = "AIzaSyBRDuu2P07VOQBVUtGd4m5KP8JB2wx3_S4"
CSE_ID = "b5a161b512cf34d20"

async def search_google(p_message_list, channel, username, is_private):
    google_channel = discord.utils.get(channel.guild.channels, name="google")
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == "google" or channel.permissions_for(username).administrator:
        query = " ".join(p_message_list[1:])
        service = build("customsearch", "v1", developerKey=API_KEY)
        result = service.cse().list(q=query, num=6, cx=CSE_ID).execute()
        items = result.get("items", [])
        description = ""
        for i, item in enumerate(items):
            description += f"Result {i+1} for '{query}': ({item['link']})\n"
        
        embed = Embed(title="Google search results", description=description, color=discord.Color.blue())
        if is_private:
            await username.send(embed=embed)
        else:
            await google_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in google channel or in a private chat")
    