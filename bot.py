import os
import discord
from discord.ext import commands
from openai import OpenAI

# ===== FLASK (Render) =====
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Eclipse bot online"

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web).start()

# ===== CONFIG =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ===== DISCORD =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== ONLINE =====
@bot.event
async def on_ready():
    print("[ECLIPSE CORE ONLINE]")
    await bot.change_presence(activity=discord.Game(name="Eclipse Control"))

# ===== TESTE =====
@bot.command()
async def ping(ctx):
    await ctx.send("🟥 Eclipse operacional.")

# ===== IA =====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if bot.user in message.mentions or message.content.lower().startswith("chat "):
        try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
Você é o Eclipse Core, uma inteligência administrativa.

- Respostas curtas e diretas
- Seja útil e objetivo
- Ignore mensagens irrelevantes
"""},
                    {"role": "user", "content": message.content}
                ],
                max_tokens=120
            )

            texto = resposta.choices[0].message.content
            await message.channel.send(texto)

        except Exception as e:
            print(f"Erro IA: {e}")
            await message.channel.send("⚠️ Erro interno.")

# ===== RUN =====
try:
    print("Iniciando bot...")
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print(f"ERRO AO INICIAR: {e}")