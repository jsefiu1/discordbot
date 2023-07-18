import discord
from discord import Embed



async def commands_telegrafi(channel, username, is_private):
    with open("app/text-files/commands_telegrafi.txt", "r") as file:
            content = file.read()
            embed = Embed(title="Telegrafi Commands", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)
                

async def help_command(channel, username, is_private):
      with open("app/text-files/help_message.txt", "r") as file:
            content = file.read()
            embed = discord.Embed(title="Help Message", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)

async def commands_gpt(channel, username, is_private):
      with open("app/text-files/commands_gpt.txt", "r") as file:
            content = file.read()
            embed = discord.Embed(title="chatGPT commands", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)

async def commands_google(channel, username, is_private):
      with open("app/text-files/commands_google.txt", "r") as file:
            content = file.read()
            embed = discord.Embed(title="Google commands", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)

async def commands_currencies(channel, username, is_private):
      with open("app/text-files/commands_currencies.txt", "r") as file:
            content = file.read()
            embed = discord.Embed(title="Convert Currencies commands", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)
                
async def commands_gjirafa(channel, username, is_private):
  with open("app/text-files/commands_gjirafa.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Gjirafa Commands", description=content, color=discord.Color.green())
    if is_private:
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)


async def commands_weather(channel, username, is_private):
  with open("app/text-files/commands_weather.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Weather Command", description=content, color=discord.Color.green())
    if is_private:
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)

async def commands_nasa(channel, username, is_private):
  with open("app/text-files/commands_nasa.txt", "r") as file:
    content = file.read()
    embed = Embed(title="Nasa Command", description=content, color=discord.Color.green())
    if is_private:
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)


async def commands_douglas(channel, username, is_private):
    with open("app/text-files/commands_douglas.txt", "r") as file:
            content = file.read()
            embed = Embed(title="Douglas Commands", description=content, color=discord.Color.green())
            if is_private:
                await username.send(embed=embed)
            else:
                await channel.send(embed=embed)