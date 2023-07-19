import requests
import discord
from discord import Embed

async def scrape_gazetaexpress(p_message_list, channel, username, is_private):

    if isinstance(channel, discord.DMChannel):
        express_channel = channel
    else:
        express_channel = discord.utils.get(channel.guild.channels, name="express")

    if isinstance(channel, discord.DMChannel) or channel.name.lower() == express_channel.name or channel.permissions_for(username).administrator:
        url_paths = [
            "lajme",
            "sport",
            "op-ed",
            "roze",
            "shneta",
        ]
        count = 0
        query_params = {}
        
        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value

        if is_private:
            await username.send("Please wait. This scraper may take a while ...")
        else:
            await express_channel.send("Please wait. This scraper may take a while ...")

        for url_path in url_paths:
            query_params["url_path"] = url_path
            response = requests.get(
                url="http://localhost:8000/gazetaexpress/scrape",
                params=query_params
            )
            count += len(response.json())
            if count >= int(argument_value):
                break

        embed = Embed(title="Scraping Status", description=f"Done: Scraped {count} articles from Express website.", color=discord.Color.red())
        if is_private:
            await username.send(embed=embed)
        else:
            await express_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in express channel or in a private chat")



async def data_express(p_message_list, channel):
    query_params={
        # "title_contains": "",
        # "offset": 0,
        
    }
    for argument in p_message_list[2:]:
        
        splitted_argument=argument.split(":")
        argument_name=splitted_argument[0]
        argument_value=splitted_argument[1]
        query_params[argument_name]=argument_value


    response = requests.get(
        url="http://localhost:8000/gazetaexpress/data",
        params=query_params
    )

    print(response)
    
    
    results = response.json()["results"]

    for result in results:
        embed = discord.Embed(
            title=result['name'],
            description=f"Scraping Date: {result['date_scraped']}",
            color=discord.Color.blue()
        )
        details_link = f"[Read More]({result['details']})"
        embed.add_field(name="", value=details_link, inline=False)
        embed.set_image(url=result['image'])
        await channel.send(embed=embed)