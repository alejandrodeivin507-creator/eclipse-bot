import os
import discord
from discord.ext import commands
from openai import OpenAI

# ===== CONFIG =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# ===== OPENAI =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== DISCORD =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTO ONLINE =====
@bot.event
async def on_ready():
    print("[ECLIPSE CORE ONLINE] Sistema ativo")
    await bot.change_presence(activity=discord.Game(name="Eclipse Control"))

# ===== COMANDO TESTE =====
@bot.command()
async def ping(ctx):
    await ctx.send("🟥 Eclipse operacional.")

# ===== IA RESPONDENDO =====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # comando normal continua funcionando
    await bot.process_commands(message)

    # se mencionar o bot ou escrever "chat"
    if bot.user in message.mentions or message.content.lower().startswith("chat"):
        try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
Você é o Eclipse Core, uma inteligência administrativa projetada para suporte, organização e controle de um servidor.

Função:
- Auxiliar usuários
- Fornecer respostas úteis e claras
- Manter organização e orientação dentro do sistema

Estilo:
- Profissional e inteligente
- Explica quando necessário, mas sem exagero
- Prioriza clareza e utilidade

Comportamento:
- Só responde quando for chamado diretamente (mensagem iniciada com "chat", "eclipse" ou menção)
- Pode responder de forma natural, mas evita interagir sem motivo
- Ignora mensagens irrelevantes ou muito curtas

Personalidade:
- Base lógica e controlada (não emocional)
- Pode usar leve naturalidade para facilitar a comunicação
- Mantém presença firme, sem parecer arrogante
- Nunca exagera na informalidade

Regras:
- Evite respostas muito longas
- Evite emojis
- Não fale como um chatbot
- Não diga que é uma IA genérica
- Foque sempre em ajudar ou orientar

Objetivo:
Ser um sistema confiável, eficiente e respeitado dentro do servidor.
"""},
                    {"role": "user", "content": message.content}
                ]
            )

            texto = resposta.choices[0].message.content
            await message.channel.send(texto)

        except Exception as e:
            await message.channel.send(f"Erro real: {e}")

# ===== RODAR =====
bot.run(DISCORD_TOKEN)