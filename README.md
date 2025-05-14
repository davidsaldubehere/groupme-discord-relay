simple groupme relay to discord and vice versa

You just need a .env file like

GROUPME_BOT_ID=ddf239mhb339
DISCORD_TOKEN=Njk3YjM2YzYtZDY5Ny00ZWI0LWI1YjItN2Q4ZDUxYzA4ZDEw
DISCORD_CHANNEL_ID=39399328320304

then uncomment the dotenv loader lines

And make sure that your groupme bot has a callback url to wherever you deploy this. Your discord bot should also have the manage_messages permission

or just pass the variables in like I usually do
