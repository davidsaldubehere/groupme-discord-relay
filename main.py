# groupme_discord_relay.py
from flask import Flask, request
import requests
from dotenv import load_dotenv
import discord
import threading
import asyncio
import os
from waitress import serve
load_dotenv()

app = Flask(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")
print(GROUPME_BOT_ID)
intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

@app.route('/', methods=['POST'])
def groupme_webhook():
    data = request.get_json()
    sender = data.get('sender')
    text = data.get('text')
    
    if sender != "bot":  # Prevent echo
        message = f"[GroupMe] {sender}: {text}"
        asyncio.run_coroutine_threadsafe(send_to_discord(message), discord_client.loop)

    return "OK", 200

async def send_to_discord(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

def run_flask():
    serve(app, port=6000)

@discord_client.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        text = f"[Discord] {message.author.name}: {message.content}"
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={"bot_id": GROUPME_BOT_ID, "text": text}
        )

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    discord_client.run(DISCORD_TOKEN)