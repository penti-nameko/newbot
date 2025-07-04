import discord
import os
from keep_alive import keep_alive # Renderでボットを稼働状態に保つためのモジュール

# --- Discordボットの設定 ---

# インテントの設定
# ボットが必要とするイベント（例: メッセージの読み取り）をDiscordに伝えます。
# message_content はメッセージの内容を読み取るために必須です。
intents = discord.Intents.default()
intents.message_content = True

# Discordクライアントの初期化
# ここで voice_client_class=None を設定することが重要です。
# これにより、音声機能に関連するエラー（audioopがないなど）を防ぎます。
client = discord.Client(intents=intents, voice_client_class=None)

# --- ボットのイベントハンドラ ---

@client.event
async def on_ready():
    """
    ボットがDiscordに正常にログインし、準備が完了したときに実行されます。
    """
    print(f'ログインしました: {client.user}')
    print('------')

@client.event
async def on_message(message):
    """
    メッセージが送信されたときに実行されます。
    """
    # ボット自身のメッセージには応答しないようにします
    if message.author == client.user:
        return

    # "$hello" というメッセージに反応して "Hello!" と返信する例
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # ここに他のボットのコマンドや機能を追加できます
    # 例: 特定のキーワードに反応する、画像を送信するなど

# --- ボットの起動 ---

# 環境変数からDiscordボットのトークンを取得します。
# Renderのウェブサービス設定で 'BOT_TOKEN' という名前でトークンを設定する必要があります。
TOKEN = os.environ.get("BOT_TOKEN")

# トークンが設定されていることを確認し、ボットを起動します。
if TOKEN:
    # keep_alive() 関数を呼び出して、ウェブサービスを継続的に稼働させます。
    # これがないと、Renderはサービスがアイドル状態だと判断して停止する可能性があります。
    keep_alive()
    
    # Discordボットを起動し、Discordサーバーに接続します。
    client.run(TOKEN)
else:
    # 環境変数が設定されていない場合のエラーメッセージ
    print("エラー: BOT_TOKEN 環境変数が設定されていません。ボットは起動できません。")
