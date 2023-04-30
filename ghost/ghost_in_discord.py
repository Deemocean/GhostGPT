import discord
import os
import openai
intents = discord.Intents(messages=True, message_content = True)
client = discord.Client(command_prefix='!',intents=intents)
from ghost import imprint

openai.api_key = None
try:
    openai.api_key = os.environ["OPENAI_KEY"]
except KeyError:
    print("No openAI token found!")
    exit()
imp = imprint.get(printing = False)
@client.event
async def on_message(message):
    if message.content.startswith("!g"):
        msg = message.content[1:]
        msg_sent =imp.chat(msg)
        print(imp.chat(msg_sent))
        
        await message.channel.send(msg_sent)
try:
    client.run(os.environ["DISCORD_TOKEN"])
except KeyError:
    print("No Discord key has been set!")