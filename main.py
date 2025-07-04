import discord
import os
from keep_alive import keep_alive # keep_alive.py をインポートしている前提です

# Discordボットが受け取るイベント（インテント）を設定します
intents = discord.Intents.default()
intents.message_content = True # メッセージの内容を読み取るために必須です。

# ここが最も重要です！ voice_client_class=None を追加してください。
# これにより、discord.py が音声関連のモジュール（audioopを含む）を読み込もうとしなくなります。
client = discord.Client(intents=intents, voice_client_class=None)

# --- ここからボットのイベントハンドラなどのコード ---

@client.event
async def on_ready():
    # ボットがDiscordにログインした際に表示されるメッセージ
    print(f'ログインしました: {client.user}')
    print('------')

@client.event
async def on_message(message):
    # ボット自身のメッセージには応答しないようにします
    if message.author == client.user:
        return

    # "$hello"というメッセージに反応する例
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# --- ここまでボットのイベントハンドラなどのコード ---

# 環境変数からDiscordボットのトークンを取得します
# Renderに BOT_TOKEN という環境変数を設定している必要があります
TOKEN = os.environ.get("BOT_TOKEN")

# トークンが設定されているか確認し、ボットを起動します
if TOKEN:
    keep_alive() # Renderのウェブサービスを稼働状態に保つためのFlaskサーバーを起動
    client.run(TOKEN) # Discordボットを起動してオンラインにします
else:
    print("エラー: BOT_TOKEN 環境変数が設定されていません。")
