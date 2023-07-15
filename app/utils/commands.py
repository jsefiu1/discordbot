import discord
from discord import Embed

async def commands_gjirafa(channel, username):
  with open("app/text-files/commands_gjirafa.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Gjirafa Commands", description=content, color=discord.Color.green())
    if isinstance(channel, discord.DMChannel):
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)

async def commands_weather(channel, username):
  with open("app/text-files/commands_weather.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Weather Command", description=content, color=discord.Color.green())
    if isinstance(channel, discord.DMChannel):
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)

async def commands_nasa(channel, username):
  with open("app/text-files/commands_nasa.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Nasa Command", description=content, color=discord.Color.green())
    if isinstance(channel, discord.DMChannel):
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)