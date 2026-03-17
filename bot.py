import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("BOT ONLINE!!!")

try:
    client.run(TOKEN)
except Exception as e:
    print("ERRO:", e)
