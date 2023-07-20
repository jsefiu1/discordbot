import requests
import random
from discord import Embed
import discord

async def generate_joke(is_private, username, channel):
   if isinstance(channel, discord.DMChannel):
        jokes_channel = channel
   else:
        jokes_channel = discord.utils.get(channel.guild.channels, name="jokes")
   if isinstance(channel, discord.DMChannel) or channel.name.lower() == jokes_channel.name or channel.permissions_for(username).administrator:
      api_url = 'https://api.api-ninjas.com/v1/jokes'
      response = requests.get(api_url, headers={'X-Api-Key': 'Phd9p+Y+cxboavZxisLzPA==RitpHwBXzM9WTgrY'})
      if response.status_code == requests.codes.ok:
         joke_data = response.json()
         random_joke = random.choice(joke_data)
         joke = random_joke['joke']
         embed = Embed(title="Joke:", color=discord.Color.blue())
         embed.add_field(name="", value=joke)
         if is_private:
            await username.send(embed=embed)
         else:
            await jokes_channel.send(embed=embed)
      else:
         return "Opps... Something went wrong!"
   else:
      await channel.send("If you are not an admin, this function can be used only in jokes channel or in a private chat")