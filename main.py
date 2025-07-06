import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.display_name}!")

keep_alive()
bot.run(TOKEN)
