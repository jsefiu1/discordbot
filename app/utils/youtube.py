from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import discord

async def search_youtube_videos(title, username, channel, is_private):
    if isinstance(channel, discord.DMChannel):
        youtube_channel = channel
    else:
        youtube_channel = discord.utils.get(channel.guild.channels, name="youtube")

    if isinstance(channel, discord.DMChannel) or channel.name.lower() == youtube_channel.name or channel.permissions_for(username).administrator:
        api_key = "AIzaSyDELoY7-WvCrPPAOObwT1B1ohhsKJ41RN4"
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_links = []

        try:
            search_response = youtube.search().list(
                q=title,
                part='snippet',
                type='video',
                maxResults=10
            ).execute()

            for search_result in search_response.get('items', []):
                video_id = search_result['id']['videoId']
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                video_links.append(f"**Link** {video_link}\n\n")

        except HttpError as e:
            print(f"Error while searching in YouTube API: {e}")

        
        if video_links:
            if is_private:
                random_video = random.choice(video_links)
                await username.send(random_video)
            else:
                random_video = random.choice(video_links)
                await youtube_channel.send(random_video)
        else:
            return "No results found"
    else:
        await channel.send("If you are not an admin, this function can be used only in youtube channel or in a private chat")