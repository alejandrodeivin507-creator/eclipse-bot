import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("BOT ONLINE!!!")

client.run(TOKEN)
