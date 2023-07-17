from discord import Embed
import discord
import openai
import os
import requests


openai.api_key = "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"

async def chatGPT_response(p_message_list, channel, username, is_private):
    if isinstance(channel, discord.DMChannel):
        chatGPT_channel = channel
    else:
        chatGPT_channel = discord.utils.get(channel.guild.channels, name="chatgpt")

    if chatGPT_channel is not None or channel.permissions_for(username).administrator:
        thumbnail_url = "https://ih1.redbubble.net/image.4645193321.0183/st,small,507x507-pad,600x600,f8f8f8.jpg"

        if p_message_list[1] == "summarize":

            response = requests.get(
            url="http://localhost:8000/telegrafi/data",
            params={"article_id":p_message_list[2]} )

            results = response.json()["results"]
            result = results[0]
            query = f"summarize this article into a more consize version in albanian: {result['details']}"

        else:
            query = " ".join(p_message_list[1:])

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant.'
                },
                {
                    'role': 'user',
                    'content': query
                }
            ],
            stream=False
        )

        if response and len(response.choices) > 0:
            query_response = response.choices[0].message.content
        embed = Embed(title="GPT chat", description=query_response, color=discord.Color.blue())
        embed.set_thumbnail(url=thumbnail_url)
        if is_private:
            await username.send(embed=embed)
        else:
            await chatGPT_channel.send(embed=embed)
    else:
        await channel.send("If you are not an admin, this function can be used only in chatgpt channel or in a private chat")