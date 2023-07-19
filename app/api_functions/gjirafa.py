import discord
import requests
from discord import Embed

async def scrape_gjirafa(p_message_list, channel, username, is_private):
   
    if isinstance(channel, discord.DMChannel):
        gjirafa_channel = channel
    else:
        gjirafa_channel = discord.utils.get(channel.guild.channels, name="gjirafa")

    if gjirafa_channel is not None or channel.permissions_for(username).administrator:
      
        url_paths = [
            "/kozmetike",
            "/aksesore",
            "/veshje",
            "/shtepi",
            "/sport",
            "/teknologji",
            "/femije",
            "/librari",
            "/vegla-pune",
            "/auto",
            "/shendet",
            "/ushqime-pije",
        ]
   
        count = 0
        query_params = {}

        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value

        for url_path in url_paths:
            if is_private:
                await username.send(f"Scraping {url_path} ...")
            else: 
                await gjirafa_channel.send(f"Scraping {url_path} ...")
            query_params["url_path"] = url_path
            response = requests.get(
                url="http://localhost:8000/gjirafa/scrape",
                params=query_params
            )
            count += len(response.json())

            embed = Embed(title="Scraping Status", description=f"Done: Scraped {count} articles from Telegrafi website.", color=discord.Color.red())

            if is_private:
                await username.send(f"Scraped {len(response.json())} articles from {url_path}")
            else:
                await gjirafa_channel.send(f"Scraped {len(response.json())} articles from {url_path}")
    else:
        await channel.send("This function will work only in gjirafa channel or private chat")



async def data_gjirafa(p_message_list, channel,username, is_private):
    if isinstance(channel, discord.DMChannel):
        gjirafa_channel = channel
    else:
        gjirafa_channel = discord.utils.get(channel.guild.channels, name="gjirafa")

    if gjirafa_channel is not None or channel.permissions_for(username).administrator:
        query_params = {}
        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value

        response = requests.get(
            url="http://localhost:8000/gjirafa/data",
            params=query_params
        )

        results = response.json()["results"]
        

        for result in results:
            name = result["name"]
            date_scraped = result["date_scraped"]
            price = result["price"]
            details_link = result["details_link"]

            embed = discord.Embed(title="**Gjirafa Data**", color=discord.Color.orange())

            embed.add_field(name="Name", value=name, inline=False)
            embed.add_field(name="Date Scraped", value=date_scraped, inline=False)
            embed.add_field(name="Price", value=price, inline=False)
            embed.add_field(name="Details", value=details_link, inline=False)

            if is_private:
                await username.send(embed=embed)
            else:
                await gjirafa_channel.send(embed=embed)
    else:
        await channel.send("This function will work only in gjirafa channel or private chat")