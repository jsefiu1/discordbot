import requests
import discord 
from discord import Embed

async def scrape_ofertasuksesi(p_message_list, channel, username, is_private):
    if isinstance(channel, discord.DMChannel):
        ofertasuksesi_channel = channel
    else:
        ofertasuksesi_channel = discord.utils.get(channel.guild.channels, name="ofertasuksesi")

    if isinstance(channel, discord.DMChannel) or channel.name.lower() == ofertasuksesi_channel.name or channel.permissions_for(username).administrator:
        url_paths = [
            "1-patundshmeri",
            "2-automjete",
            "3-rreth-punes",
            "4-pc-tv-etj",
            "5-celular",
            "6-shtepia-juaj",
            "7-bashkepunim",
            "8-sherbime",
            "9-bujqesi",
            "10-kafshe",
            "11-interesi-juaj",
            "12-te-ndryshme",
            ]
        query_params = {}

        for argument in p_message_list[2:]: 
            splitted_argument = argument.split(":")  
            argument_name = splitted_argument[0]  
            argument_value = splitted_argument[1]
            query_params[argument_name] = argument_value

        if is_private:
            await username.send(f"Please wait this scrape might take a while...")
        else:
            await ofertasuksesi_channel.send("Please wait this scrape might take a while...")

        count = 0
        for url_path in url_paths:
            query_params["category"] = url_path
            response = requests.post(url="http://localhost:8000/ofertasuksesi/scrape", params=query_params)
            count += len(response.json())
        
        embed = Embed(title="Scraping Status", description=f"Done: Scraped {count} offers from ofertasuksesi", color=discord.Color.red())

        if is_private:
            await username.send(embed=embed)
        else:
            await ofertasuksesi_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in ofertasuksesi channel or in a private chat")


async def data_ofertasuksesi(p_message_list, channel, username, is_private):
    if isinstance(channel, discord.DMChannel):
        ofertasuksesi_channel = channel
    else:
        ofertasuksesi_channel = discord.utils.get(channel.guild.channels, name="ofertasuksesi")
    
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == ofertasuksesi_channel.name or channel.permissions_for(username).administrator:
        query_params={}
        for argument in p_message_list[2:]:
            splitted_argument=argument.split(":")
            argument_name=splitted_argument[0]
            argument_value=splitted_argument[1]
            query_params[argument_name]=argument_value


        response = requests.get(
            url="http://localhost:8000/ofertasuksesi/data",
            params=query_params
        )
        
        
        results = response.json()["results"]

        for result in results:
            embed = discord.Embed(title=f"Title: \n{result['title']}",description=f"**Description**: \n{result['info']}",color=discord.Color.blue())
            embed.set_thumbnail(url=result["image"])
            embed.add_field(name="Location", value=result['location'], inline=False)

            # Shtimi i foton në Embed
            if 'featured-image' in result:
                embed.set_thumbnail(url=result['featured-image'])

            if is_private:
                await username.send(embed=embed)
            else:
                await ofertasuksesi_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in ofertasuksesi channel or in a private chat")