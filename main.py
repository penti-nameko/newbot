import os
import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive # keep_alive.py から keep_alive 関数をインポート

# --- Discord Botの設定 ---
# 環境変数からボットのトークンを取得
# Render.comの環境変数に 'BOT_TOKEN' としてDiscordボットのトークンを設定してください。
TOKEN = os.getenv('BOT_TOKEN')

# Discordのインテントを設定
# メッセージの内容を読み取るために message_content インテントを有効にします。
# Discord開発者ポータルでPrivileged Gateway IntentsのMessage Content Intentも有効にしてください。
intents = discord.Intents.default()
intents.message_content = True

# コマンドプレフィックスを '!' に設定
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    ボットがDiscordに正常にログインし、準備ができたときに実行されます。
    """
    print(f"ログインしました: {bot.user.name} (ID: {bot.user.id})")
    print("---------------------------------------")

@bot.command()
async def hello(ctx):
    """
    '!hello' コマンドに応答します。
    例: ユーザーが '!hello' と入力すると、ボットが 'Hello [ユーザー名]!' と返信します。
    """
    await ctx.send(f"Hello {ctx.author.display_name}!")

# --- ボットの起動ロジック ---
async def main():
    """
    Discordボットを非同期で起動します。
    keep_aliveサーバーは別で起動されます。
    """
    # Discordボットを起動
    if TOKEN:
        try:
            await bot.start(TOKEN)
        except discord.LoginFailure:
            print("エラー: Discordボットのトークンが無効です。")
            print("環境変数 'BOT_TOKEN' を確認してください。")
        except discord.HTTPException as e:
            if e.status == 429:
                print(f"エラー: Discord APIからのレート制限です。しばらく待ってから再試行してください。詳細: {e}")
            else:
                print(f"Discord HTTPエラーが発生しました: {e}")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
    else:
        print("エラー: 環境変数 'BOT_TOKEN' が設定されていません。")

if __name__ == "__main__":
    # keep_aliveサーバーを先に起動
    keep_alive() # keep_alive.py からインポートされた関数を呼び出す
    print("Keep-aliveサーバーを起動しました。")

    # その後、Discordボットを非同期で起動
    asyncio.run(main())
