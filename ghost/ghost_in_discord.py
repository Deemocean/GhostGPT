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
    if message.content.startswith("!ghost"):
        msg = message.content[6:]
        if msg == "eject":
            exit()
        else:
            await message.channel.send(imp.chat(msg))
try:
    client.run(os.environ["DISCORD_TOKEN"])
except KeyError:
    print("No Discord key has been set!")