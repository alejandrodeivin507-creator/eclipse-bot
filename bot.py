import os
import discord
from discord.ext import commands

# ===== DEBUG INICIAL =====
print("Iniciando aplicação...")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Token carregado?", "SIM" if DISCORD_TOKEN else "NÃO")
print("OpenAI Key carregada?", "SIM" if OPENAI_API_KEY else "NÃO")

# ===== FLASK (Render) =====
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Eclipse bot online"

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web, daemon=True).start()

# ===== DISCORD =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== OPENAI (OPCIONAL) =====
use_ai = False
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        use_ai = True
        print("OpenAI inicializado com sucesso")
    except Exception as e:
        print("Erro ao iniciar OpenAI:", e)

# ===== EVENTOS =====
@bot.event
async def on_ready():
    print("[ECLIPSE CORE ONLINE]")
    await bot.change_presence(activity=discord.Game(name="Eclipse Control"))

# ===== COMANDO TESTE =====
@bot.command()
async def ping(ctx):
    await ctx.send("🟥 Eclipse operacional.")

# ===== IA =====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not use_ai:
        return

    if bot.user in message.mentions or message.content.lower().startswith("chat "):
        try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Responda de forma curta, direta e útil."},
                    {"role": "user", "content": message.content}
                ],
                max_tokens=120
            )

            texto = resposta.choices[0].message.content
            await message.channel.send(texto)

        except Exception as e:
            print("Erro IA:", e)
            await message.channel.send("⚠️ Falha na IA.")

# ===== RUN =====
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN NÃO CONFIGURADO NO RENDER")

print("Conectando ao Discord...")
bot.run(DISCORD_TOKEN)
