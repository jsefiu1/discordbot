import discord
import requests

async def create_gjirafa_embed(results):
    embed = discord.Embed(title="**Gjirafa Data Result**", color=discord.Color.orange())
    
    if results is not None:
        for result in results:
            name = result["name"]
            date_scraped = result["date_scraped"]
            price = result["price"]
            details_link = result["details_link"]
            
            embed.add_field(name="Name", value=name, inline=True)
            embed.add_field(name="Date Scraped", value=date_scraped, inline=True)
            embed.add_field(name="Price", value=price, inline=True)
            embed.add_field(name="Details", value=details_link, inline=False)
    else:
        embed.description = "No results found."

    return embed

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
        embed = await create_gjirafa_embed(results)
        await channel.send(embed=embed)
    else:
        await channel.send("Failed to retrieve data.")
