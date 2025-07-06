import discord
from discord.ext import commands
import os
import requests # requestsライブラリを追加
from keep_alive import keep_alive

# 環境変数からTenor APIキーを取得
TENOR_API_KEY = os.getenv('TENOR_API_KEY') # 環境変数にTENOR_API_KEYを追加してください

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

@bot.command()
async def gif(ctx, *, search_query: str):
    """
    キーワードに基づいてGIFを検索・表示します。
    例: !gif funny cat
    """
    if not TENOR_API_KEY:
        await ctx.send("Tenor APIキーが設定されていません。")
        return

    url = f"https://api.tenor.com/v1/search?q={search_query}&key={TENOR_API_KEY}&limit=1"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data['results']:
            gif_url = data['results'][0]['media'][0]['gif']['url']
            await ctx.send(gif_url)
        else:
            await ctx.send(f"'{search_query}' に関連するGIFは見つかりませんでした。")
    except Exception as e:
        await ctx.send(f"GIFの検索中にエラーが発生しました: {e}")

keep_alive()
bot.run(TOKEN)
