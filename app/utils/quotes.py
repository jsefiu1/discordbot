import requests
from discord import Embed
import discord

async def generate_quote(username, channel, is_private):
    if isinstance(channel, discord.DMChannel):
        quotes_channel = channel
    else:
        quotes_channel = discord.utils.get(channel.guild.channels, name="quotes")
   
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == quotes_channel.name or channel.permissions_for(username).administrator:
        response = requests.get('https://api.quotable.io/random')
        data = response.json()

        if 'content' in data and 'author' in data:
            quote = data['content']
            author = data['author']
            embed = Embed(title=f"Quote:", description=quote, color=discord.Color.blue())
            embed.add_field(name="Author:", value=author)
            if is_private:
                # await quotes_channel.send("**CHECK DM**")
                await username.send(embed=embed)
            else:
                await quotes_channel.send(embed=embed)
        else:
            return 'Unable to fetch quote'
    else:
        await channel.send("If you are not an admin, this function can be used only in ofertasuksesi channel or in a private chat")