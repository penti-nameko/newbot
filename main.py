import os
import discord
from dotenv import load_dotenv # .env ファイルから環境変数を読み込むために必要

# Flaskサーバーのインポート（keep_alive.py を使用している場合）
from keep_alive import keep_alive

# .env ファイルを読み込む
# Renderでは環境変数を直接設定するため、この行は主にローカルテスト用ですが、
# コードに残しておくのは問題ありません。
load_dotenv()

# Discordボットのトークンを環境変数から取得
TOKEN = os.getenv('BOT_TOKEN')

# intents（インテント）の設定
# これが非常に重要です！ボットがどのようなイベントを受信するかを定義します。
# 必要な権限をDiscord開発者ポータルで有効にし、ここでも設定します。
intents = discord.Intents.default()
# 一般的なボットでメッセージの内容を読み取るには以下が必須
intents.message_content = True
# メンバーリストやプレゼンス（オンライン状態など）が必要な場合
# intents.members = True # GUILD MEMBERS INTENT をDiscord開発者ポータルで有効にする必要あり
# intents.presences = True # PRESENCE INTENT をDiscord開発者ポータルで有効にする必要あり

# Discordクライアントの初期化
# ★★★ ここが重要！音声機能を使わないなら 'voice_client_class=None' を追加 ★★★
client = discord.Client(intents=intents, voice_client_class=None) # これを追加！

# ボットが起動したときに実行されるイベント
@client.event
async def on_ready():
    print(f'ログインしました: {client.user}') # このメッセージがログに出たら成功！
    print(f'ユーザーID: {client.user.id}')
    print('------')

# メッセージを受信したときに実行されるイベント
@client.event
async def on_message(message):
    # ボット自身のメッセージは無視
    if message.author == client.user:
        return

    # "hello" に応答する例
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

# Keep-aliveサーバーを別スレッドで起動（Renderの無料プランでボットを稼働させ続けるため）
keep_alive()

# Discordボットを実行
# TOKENがNone（設定されていない）の場合、エラーを出すようにする
if TOKEN is None:
    print("エラー: 環境変数 'BOT_TOKEN' が設定されていません。ボットを起動できません。")
else:
    try:
        client.run(TOKEN) # ボットトークンでログインを試みる
    except discord.errors.LoginFailure:
        print("エラー: Discordボットのトークンが無効です。")
        print("Discord開発者ポータルでトークンをリセットし、Renderの環境変数を再確認してください。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
