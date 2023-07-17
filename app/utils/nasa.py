import requests
import discord

API_KEY = "8wUgXmiNbUPEprFLFV5iomC68uESxv440NcBlxKw"
BASE_URL = "https://api.nasa.gov/planetary/apod"

async def process_nasa_command(p_message_list, channel,username, is_private):
 
    if isinstance(channel, discord.DMChannel):
        nasa_channel = channel
    else:
        nasa_channel = discord.utils.get(channel.guild.channels, name="nasa")

    if nasa_channel is not None or channel.permissions_for(username).administrator:

        url = None
        num_days = 1

        if len(p_message_list) >= 2:
            if p_message_list[1] == "random":
                url = f"{BASE_URL}?api_key={API_KEY}&count=1"
            else:
                query = " ".join(p_message_list[1:])
                url = f"{BASE_URL}?api_key={API_KEY}&count=10"

        if url is None:
            return "Please provide a command or query for the NASA command."

        try:
            response = requests.get(url)
            response.raise_for_status()
            apod_data = response.json()
            
            if len(apod_data) == 0:
                return "No APOD found."

            embed = discord.Embed(title="NASA Astronomy Picture of the Day", color=discord.Color.blue())

            if p_message_list[1] == "random":
                item = apod_data[0]
            else:
                filtered_data = [
                    item for item in apod_data
                    if query.lower() in item.get("title", "").lower()
                    or query.lower() in item.get("explanation", "").lower()
                ]

                if len(filtered_data) == 0:
                    return f"No APOD found related to '{query}'."
                
                item = filtered_data[0]

            title = item.get("title", "")
            explanation = item.get("explanation", "")
            image_url = item.get("url", "")

            truncated_title = title[:256] + "..." if len(title) > 256 else title
            truncated_explanation = explanation[:512] + "..." if len(explanation) > 512 else explanation

            embed.add_field(name="Title", value=truncated_title, inline=False)
            embed.add_field(name="Explanation", value=truncated_explanation, inline=False)
            embed.set_image(url=image_url)
            embed.add_field(name="\u200b", value="\u200b", inline=False)

            result = embed

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            result = "Unable to fetch APOD data. Please try again later."

        if is_private:
            await username.send(embed=embed)
        else:
            await nasa_channel.send(embed=embed)
    else:
        await channel.send("This command only will work in channel nasa or private")