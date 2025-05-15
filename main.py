# groupme_discord_relay.py
from flask import Flask, request
import requests
#from dotenv import load_dotenv
import discord
import threading
import asyncio
import os
from waitress import serve
from io import BytesIO
#load_dotenv()

app = Flask(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")
GROUPME_ACCESS_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

@app.route('/', methods=['GET', 'POST'])
def groupme_webhook():
    if request.method == 'POST':
        data = request.get_json()
        sender = data.get('name')
        text = data.get('text', '')
        attachments = data.get('attachments', [])
        
        if data.get('sender_type') != "bot":  # Prevent echo
            message = f"{sender}: {text}"
            image_urls = []
            
            # Extract image URLs from attachments
            for attachment in attachments:
                if attachment.get('type') == 'image':
                    image_url = attachment.get('url')
                    if image_url:
                        image_urls.append(image_url)
            
            asyncio.run_coroutine_threadsafe(send_to_discord(message, image_urls), discord_client.loop)

        return "OK", 200

    elif request.method == 'GET':
        return "OK", 200

async def send_to_discord(message, image_urls=None):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        if not image_urls:
            await channel.send(message)
        else:
            # Send text first
            if message:
                await channel.send(message)
            
            # Send each image
            for url in image_urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        image_data = BytesIO(response.content)
                        file = discord.File(fp=image_data, filename="image.png")
                        await channel.send(file=file)
                except Exception as e:
                    await channel.send(f"Error sending image: {str(e)}")

def run_flask():
    serve(app, port=8080)

@discord_client.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        text = f"{message.author.display_name}: {message.content}"
        
        # Handle Discord attachments (images)
        image_urls = []
        for attachment in message.attachments:
            if attachment.content_type and 'image' in attachment.content_type:
                image_urls.append(attachment.url)
        
        # If there are images, include them in the GroupMe message
        if image_urls:
            for img_url in image_urls:
                try:
                    # Download the image
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        # Upload to GroupMe Image Service
                        groupme_img_response = requests.post(
                            "https://image.groupme.com/pictures",
                            data=response.content,
                            headers={"Content-Type": "image/png", "X-Access-Token": GROUPME_ACCESS_TOKEN}
                        )
                        
                        if groupme_img_response.status_code == 200:
                            img_url = groupme_img_response.json().get('payload', {}).get('url')
                            if img_url:
                                # Send message with image
                                requests.post(
                                    "https://api.groupme.com/v3/bots/post",
                                    json={
                                        "bot_id": GROUPME_BOT_ID, 
                                        "text": text,
                                        "attachments": [
                                            {
                                                "type": "image",
                                                "url": img_url
                                            }
                                        ]
                                    }
                                )
                                return
                except Exception as e:
                    print(f"Error handling Discord image: {str(e)}")
        
        # If no images or image upload failed, just send the text
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={"bot_id": GROUPME_BOT_ID, "text": text}
        )

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    discord_client.run(DISCORD_TOKEN)