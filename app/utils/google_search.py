import discord
import asyncio
from discord import Embed
from googlesearch import search


async def search_google(p_message_list, channel, username, is_private):
    query = " ".join(p_message_list[1:])
    results = list(search(query, num_results=10))[:3]
    for i, result in enumerate(results):
        embed = Embed(title="Google search results", color=discord.Color.blue())
        embed.add_field(name=f"Result {i+1} for '{query}':", value=result)
        if is_private:
            await username.send(embed=embed)
        else:
            await channel.send(embed=embed)
        await asyncio.sleep(5)