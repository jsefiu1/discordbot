import requests
from discord import Embed
import discord

async def get_movie_info(movie_title, username, channel, is_private):
  if isinstance(channel, discord.DMChannel):
      movies_channel = channel
  else:
      movies_channel = discord.utils.get(channel.guild.channels, name="movies")
    
  if isinstance(channel, discord.DMChannel) or channel.name.lower() == movies_channel.name or channel.permissions_for(username).administrator: 
    api_key = "aded79d8"
    base_url = f"http://www.omdbapi.com/?apikey={api_key}"
    params = {"t": movie_title}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["Response"] == "True":
      year = data["Year"]
      genre = data["Genre"]
      plot = data["Plot"]
      rating = data["imdbRating"]

      embed = Embed(title=f"Information about the film", description=plot, color=discord.Color.blue())
      embed.add_field(name=f"**Released on**:", value=year)
      embed.add_field(name=f"**Type**:", value=genre)
      embed.add_field(name=f"**Rating:**:", value=rating)

      if is_private:
        await username.send(embed=embed)
      else:
          await movies_channel.send(embed=embed)
    else:
        channel.send(f"No data found for {movie_title} film!")
  else:
      await channel.send("If you are not an admin, this function can be used only in movies channel or in a private chat")