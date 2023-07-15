import discord

async def process_command_result(channel, result):
    if isinstance(result, discord.Embed):
        await channel.send(embed=result)
    else:
        await channel.send(result)
