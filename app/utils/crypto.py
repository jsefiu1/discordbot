import requests
import re
import discord

async def get_crypto_info(crypto_name, username, channel, is_private):
    if isinstance(channel, discord.DMChannel):
        crypto_channel = channel
    else:
        crypto_channel = discord.utils.get(channel.guild.channels, name="crypto")
    
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == crypto_channel.name or channel.permissions_for(username).administrator:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            text = data['description']['en']
            text = re.sub(r'<a.*?>.*?</a>', '', text)  # Fsheh elementin HTML <a>
            embed = discord.Embed(title=f"**{crypto_name} Information**", description=f"**Description**:{text}",color=discord.Color.blue())
            embed.add_field(name=f"Name:", value=data['name'])
            embed.add_field(name=f"Symbol:", value=data['symbol'])
            embed.add_field(name="Current price:", value=data['market_data']['current_price']['usd'])
            embed.set_thumbnail(url=data['image']['large'])

            if is_private:
                await username.send(embed=embed)
            else:
                await crypto_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in ofertasuksesi channel or in a private chat")
