simple groupme relay to discord and vice versa

You just need a .env file like

GROUPME_BOT_ID=ddf239mhb339
DISCORD_TOKEN=Njk3YjM2YzYtZDY5Ny00ZWI0LWI1YjItN2Q4ZDUxYzA4ZDEw
DISCORD_CHANNEL_ID=39399328320304
GROUPME_ACCESS_TOKEN=y93c79a8e7902YzYtZDY5Ny00ZWI0LWIfYjItN2Q4ZDUxYzA4ZDEw

then uncomment the dotenv loader lines

And make sure that your groupme bot has a callback url to wherever you deploy this. Your discord bot should also have the manage_messages permission.

I just use google cloud run for this but that can be finicky.

## Features

- Text message relay between GroupMe and Discord
- Image transfer support - images sent in either platform will be relayed to the other

## Getting a GroupMe Access Token

To enable image transfers from Discord to GroupMe, you'll need a GroupMe access token. You can get one by:

1. Going to https://dev.groupme.com/
2. Log in with your GroupMe account
3. Navigate to "Access Token" in your developer account
4. Copy the token and add it to your .env file

or just pass the variables in like I usually do
