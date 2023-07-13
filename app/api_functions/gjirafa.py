import discord
import requests

async def scrape_gjirafa(p_message_list, channel):
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
        await channel.send(f"Scraping {url_path} ...")
        query_params["url_path"] = url_path
        response = requests.get(
            url="http://localhost:8000/gjirafa/scrape",
            params=query_params
        )
        count += len(response.json())
        await channel.send(f"Scraped {len(response.json())} articles from {url_path}")

    return f"```Done: Scraped {count} articles```"

async def create_gjirafa_embed(results):
    embed = discord.Embed(title="**Gjirafa Data Result**", color=discord.Color.orange())
    embeds = []
    total_characters = 0
    
    if results is not None:
        for result in results:
            name = result["name"]
            date_scraped = result["date_scraped"]
            price = result["price"]
            details_link = result["details_link"]
            
            field_value = f"Name: {name}\nDate Scraped: {date_scraped}\nPrice: {price}\nDetails: {details_link}"
            if total_characters + len(field_value) > 6000:
                embeds.append(embed)
                embed = discord.Embed(title="**Gjirafa Data Result**", color=discord.Color.orange())
                total_characters = 0
            
            embed.add_field(name="\u200b", value=field_value, inline=False)
            total_characters += len(field_value)
            
        embeds.append(embed)
    else:
        embed.description = "No results found."
        embeds.append(embed)

    return embeds

async def data_gjirafa(p_message_list, channel):
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

    if response.status_code == 200:
        results = response.json()["results"]
        embeds = await create_gjirafa_embed(results)
        
        for embed in embeds:
            await channel.send(embed=embed)
    else:
        await channel.send("Failed to retrieve data.")
