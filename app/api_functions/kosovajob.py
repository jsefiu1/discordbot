import discord
import requests
from discord import Embed


async def scrape_kosovajobs(p_message_list, channel,username,is_private):
    if isinstance(channel, discord.DMChannel):
        kosovajob_channel = channel
    else:
        kosovajob_channel = discord.utils.get(channel.guild.channels, name="kosovajobs")

    if isinstance(channel,discord.DMChannel) or channel.name.lower()==kosovajob_channel.name or channel.permissions_for(username).administrator:
        scrape_url = "http://localhost:8000/kosovajobs/scrape?url_path=https%3A%2F%2Fkosovajob.com%2F"

        response = requests.get(scrape_url)

        if response.status_code == 200:
            embed = Embed(title="Scraping Status", description=f"Done: Scraped jobs from Kosovajobs website.",
                        color=discord.Color.red())
            if is_private:
                await username.send(embed=embed)
            else:
                await kosovajob_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in kosovajob channel or in a private chat")




async def data_kosovajob(p_message_list, channel,username,is_private):
    if isinstance(channel, discord.DMChannel):
        kosovajob_channel = channel
    else:
        kosovajob_channel = discord.utils.get(channel.guild.channels, name="kosovajobs")
    if isinstance(channel,discord.DMChannel) or channel.name.lower()==kosovajob_channel.name or channel.permissions_for(username).administrator:
        query_params = {}
        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value

        url = "http://localhost:8000/kosovajobs/data"
        response = requests.get(url, params=query_params)

        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                for result in results:
                    embed = discord.Embed(title="Kosovajob data")
                    embed.add_field(name="Job Title", value=result["title"], inline=False)
                    embed.add_field(name="City", value=result["city"], inline=True)
                    embed.add_field(name="Details link", value=result["details_link"], inline=False)
                    embed.set_thumbnail(url=result["image_url"])
                    
                    if is_private:
                        await username.send(embed=embed)
                    else:
                        await kosovajob_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in kosovajob channel or in a private chat")
             