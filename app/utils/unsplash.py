import requests
from io import BytesIO
import discord
from discord import Embed

async def generate_image(img_name, channel, username, is_private):
    if isinstance(channel, discord.DMChannel):
        image_channel = channel
    else:
        image_channel = discord.utils.get(channel.guild.channels, name="images")
    if isinstance(channel, discord.DMChannel) or channel.name.lower() == image_channel.name or channel.permissions_for(username).administrator:
        ACCESS_KEY = '0voRhwXoBCVzZEiRaKRpl1Vyo7rlUfWJZVvavOwJkT8'
        url = f'https://api.unsplash.com/photos/random?query={img_name}&client_id={ACCESS_KEY}'

        response = requests.get(url)
        data = response.json()

        if 'errors' in data:
            print('Something went wrong!')
            print(data['errors'][0]['detail'])
            return None

        else:
            image_url = data['urls']['regular']
            response = requests.get(image_url)
            image_data = response.content

            if image_data:
                image_buffer = BytesIO(image_data)
                file = discord.File(fp=image_buffer, filename='image.jpg')
                embed = Embed(title="The image you searched for:", color=discord.Color.blue())
                embed.set_image(url='attachment://image.jpg')  # Vendosja e fajllit të bashkangjitur si imazh në Embed
                
                if is_private:
                    # await image_channel.send("**CHECK DM**")
                    await username.send(file=file, embed=embed)
                else:
                    await image_channel.send(file=file, embed=embed)
            else:
                return "Image not found"
    else:
        await channel.send("If you are not an admin, this function can be used only in ofertasuksesi channel or in a private chat")