import requests
import discord
from discord import Embed
import datetime
from PIL import Image
import io

async def scrape_douglas(p_message_list, channel, username, is_private):
    douglas_channel = discord.utils.get(channel.guild.channels, name = "douglas")
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == "douglas" or channel.permissions_for(username).administrator:
        url_paths = [
                 "brands",
                 "parfum/01",
                 "Make-up/03",
                 "gesicht/12",
                 "koerper/13",
                 "haare/14",
                 "apotheke-gesundheit/07",
                 "home-lifestyle/15",
                 "sale/05",
                 "nachhaltigkeit/59",
                 "sommer/86",
                 "pride/90",
                 "luxuswelt/29",
                 "neuheiten/09"]
        count = 0
        query_params = {}
        
        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value
            
        if is_private:
            await username.send("Please wait. The scraper may take a while.")
        else:
            await douglas_channel.send("Please wait. The scraper may take a while.")
            
        for url_path in url_paths:
            query_params["url_path"] = url_path
            response = requests.get(
                url="http://localhost:8000/douglas/scrape",
                params=query_params
            )
            count += len(response.json())
            
        embed = Embed(title="Scraping Status", description=f"Done: Scraped {count} products from Douglas website.", color=discord.Color.red())
        if is_private:
            await username.send(embed=embed)
        else:
            await douglas_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in douglas channel or in a private chat")

async def data_douglas(p_message_list, channel, username, is_private):
    douglas_channel = discord.utils.get(channel.guild.channels, name="douglas")
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == "douglas" or channel.permissions_for(username).administrator:
        query_params = {}
        for argument in p_message_list[2:]:
            splitted_argument = argument.split(":")
            argument_name = splitted_argument[0]
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value
            
        response = requests.get(
            url="http://localhost:8000/douglas/data",
            params=query_params

        )
        
        results = response.json()["results"]
        
        for result in results:
            price = result["price"]
            category = result["category"]
            date_scraped = datetime.datetime.strptime(result['date_scraped'], "%Y-%m-%dT%H:%M:%S.%f")
            formatted_date_s = date_scraped.strftime("%Y-%m-%d %H:%M")            
            
            
            embed = Embed(title=f"{result['name']}", description=f"Product ID: {result['id']}\nScraping Date: {formatted_date_s}", color=discord.Color.blue())
            embed.add_field(name="Category", value=category, inline=False)
            embed.add_field(name="Price", value=price, inline=False)
            embed.add_field(name="Details Link", value=f"{result['details_link']}")
            embed.set_thumbnail(url="attachment://thumbnail.png")
            
            image_response = requests.get(result['image_link'])
            image = Image.open(io.BytesIO(image_response.content))
            thumbnail_size = (400, 400) 
            image = image.resize(thumbnail_size)
            thumbnail_bytes = io.BytesIO()
            image.save(thumbnail_bytes, format='PNG')
            thumbnail_bytes.seek(0)
              
            
            file = discord.File(thumbnail_bytes, filename='thumbnail.png')
            
            if is_private:
                await username.send(file=file, embed=embed)
            else:
                await douglas_channel.send(file=file, embed=embed)
        else:
            await channel.send("If you are not an admin, this function can be used only in douglas channel or in a private chat")