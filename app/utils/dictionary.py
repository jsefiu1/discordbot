import requests
from discord import Embed
import discord

async def search_word_definition(word, channel, username, is_private):
    if isinstance(channel, discord.DMChannel):
        define_channel = channel
    else:
        define_channel = discord.utils.get(channel.guild.channels, name="define")
    
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == define_channel.name or channel.permissions_for(username).administrator:
        url = f"https://api.urbandictionary.com/v0/define?term={word}"
        response = requests.get(url)
        
        if response.status_code == requests.codes.ok:
            data = response.json()
            
            if data["list"]:
                definitions = [result["definition"] for result in data["list"]]
                embed = Embed(title=f"Definition for {word}", color=discord.Color.blue())
                
                for i, definition in enumerate(definitions):
                    embed.add_field(name=f"Definition {i+1}", value=definition, inline=False)
                
                if is_private:
                    await username.send(embed=embed)
                else:
                    await define_channel.send(embed=embed)
            else:
                return f"No definitions found for '{word}'."
        else:
            return "Something went wrong!"
    else:
        await channel.send("If you are not an admin, this function can be used only in define channel or in a private chat")