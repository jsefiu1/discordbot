import requests
import discord
from discord import Embed
import datetime
from PIL import Image
import io

async def scrape_telegrafi(p_message_list, channel, username, is_private):
    url_paths = [
        "/lajme/",
        "/sport/",
        "/fun/",
        "/teknologji/",
        "/auto/",
        "/kuzhina/",
        "/shendetesi/",
        "/stili/",
        "/femra/",
        "/kultura/",
        "/magazina/",
        "/ekonomi/",
        "/bote/",
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
        await channel.send("Please wait. This scraper may take a while ...")

    for url_path in url_paths:
        query_params["url_path"] = url_path
        response = requests.get(
            url="http://localhost:8000/telegrafi/scrape",
            params=query_params
        )
        count += len(response.json())

    embed = Embed(title="Scraping Status", description=f"Done: Scraped {count} articles from Telegrafi website.", color=discord.Color.red())
    if is_private:
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)


async def data_telegrafi(p_message_list, channel, username, is_private):
    query_params = {}
    for argument in p_message_list[2:]:
        splitted_argument = argument.split(":")
        argument_name = splitted_argument[0]
        argument_value = splitted_argument[1]
        query_params[argument_name] = argument_value

    response = requests.get(
        url="http://localhost:8000/telegrafi/data",
        params=query_params
    )
    
    results = response.json()["results"]

    for result in results:
        date_scraped = datetime.datetime.strptime(result['date_scraped'], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date_s = date_scraped.strftime("%Y-%m-%d %H:%M")
        date_posted = datetime.datetime.strptime(result['date_posted'], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date_p = date_posted.strftime("%Y-%m-%d %H:%M")


        image_response = requests.get(result['image_link'])
        image = Image.open(io.BytesIO(image_response.content))
        thumbnail_size = (400, 400) 
        image = image.resize(thumbnail_size)
        thumbnail_bytes = io.BytesIO()
        image.save(thumbnail_bytes, format='PNG')
        thumbnail_bytes.seek(0)

        embed = Embed(title=f"{result['name']}", description=f"Article ID: {result['id']}\nScraping Date: {formatted_date_s}\nDate Posted: {formatted_date_p}", color=discord.Color.blue())
        embed.add_field(name="Details Link", value=f"{result['details_link']}")
        embed.set_thumbnail(url="attachment://thumbnail.png")  
        
        file = discord.File(thumbnail_bytes, filename='thumbnail.png')
        
        if is_private:
            await username.send(file=file, embed=embed)
        else:
            await channel.send(file=file, embed=embed)
