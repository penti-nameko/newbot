import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# 環境変数からBotのトークンを取得
TOKEN = os.getenv('BOT_TOKEN')

# ユーザーごとの通知を保存する辞書（Botのメモリ上に保持されるため、再起動で消えます）
# 形式: {ユーザーID: [通知1, 通知2, ...]}
user_notifications = {}

# 必要なインテントを有効にする
intents = discord.Intents.default()
intents.members = True          # メンバー情報を取得するために必要
intents.message_content = True  # メッセージ内容を読み取るために必要（従来のコマンド用）

# Botオブジェクトを作成
bot = commands.Bot(command_prefix="!", intents=intents)

# スラッシュコマンドツリーの作成
tree = commands.Tree(bot)

@bot.event
async def on_ready():
    """BotがDiscordにログインし、準備ができたときに実行されます。"""
    print(f'Botとしてログインしました: {bot.user}')
    # Botが起動したときにスラッシュコマンドをDiscordに同期
    await tree.sync()
    print("スラッシュコマンドを同期しました。")

# --- 従来のコマンド ---

@bot.command()
async def hello(ctx):
    """
    Botが挨拶を返します。
    例: !hello
    """
    await ctx.send(f"Hello {ctx.author.display_name}!")

# --- スラッシュコマンド：通知送信 ---

@tree.command(name="notification", description="ユーザーに通知を送信します。")
@discord.app_commands.describe(
    target_type="通知の送信先 (all または role)",
    message_content="通知として送信するメッセージの内容",
    role_name="通知を送信するロールの名前 (target_typeが'role'の場合のみ)"
)
async def notification(interaction: discord.Interaction, target_type: str, message_content: str, role_name: str = None):
    """
    `/notification` コマンド
    - `target_type`: "all" または "role" を指定
    - `message_content`: 通知メッセージの内容
    - `role_name`: "role" を選択した場合にロール名を指定
    """
    await interaction.response.defer(ephemeral=True) # コマンド実行者のみに見える応答

    target_channel = interaction.channel 

    # --- 通知データの保存ロジックを追加 ---
    # ここではBotのメモリに保存します。永続化にはデータベースが必要です。

    if target_type == "all":
        # 全てのサーバーメンバーに通知を保存（Bot自身は除く）
        for member in interaction.guild.members:
            if not member.bot:
                user_notifications.setdefault(member.id, []).append(f"[全体通知] {message_content}")
        
        await target_channel.send(f"@everyone {message_content}")
        await interaction.followup.send("全てのユーザーに通知を送信しました。")
        print(f"全体通知を送信: '{message_content}'")

    elif target_type == "role":
        if not role_name:
            await interaction.followup.send("ロール名を指定してください。例: `/notification role:管理者 message_content:重要な連絡です`")
            return

        target_role = discord.utils.get(interaction.guild.roles, name=role_name)

        if target_role:
            # 指定されたロールのメンバーに通知を保存
            for member in target_role.members:
                if not member.bot:
                    user_notifications.setdefault(member.id, []).append(f"[{target_role.name}向け] {message_content}")
            
            await target_channel.send(f"{target_role.mention} {message_content}")
            await interaction.followup.send(f"ロール「**{role_name}**」のユーザーに通知を送信しました。")
            print(f"ロール '{role_name}' へ通知を送信: '{message_content}'")
        else:
            await interaction.followup.send(f"ロール「**{role_name}**」が見つかりません。")
            print(f"ロール '{role_name}' が見つかりませんでした。")
    else:
        await interaction.followup.send("無効なターゲットタイプです。「**all**」または「**role**」を指定してください。")
        print("無効なターゲットタイプが指定されました。")

# --- スラッシュコマンド：通知一覧表示 ---

@tree.command(name="smartphone", description="あなたの通知一覧を表示します。")
async def smartphone(interaction: discord.Interaction):
    """
    `/smartphone` コマンド
    コマンドを実行したユーザーの通知一覧をDMで送信します。
    """
    user_id = interaction.user.id
    
    # ユーザーの通知を取得
    notifications = user_notifications.get(user_id, [])

    if notifications:
        # 通知がある場合、整形してDMで送信
        notification_list = "\n".join([f"- {n}" for n in notifications])
        try:
            await interaction.user.send(f"あなたの通知一覧です:\n{notification_list}")
            await interaction.response.send_message("あなたの通知一覧をDMに送信しました。", ephemeral=True)
            print(f"{interaction.user.display_name} ({user_id}) に通知一覧を送信しました。")
            
            # 通知を一度表示したらクリアする場合（オプション）
            # user_notifications[user_id] = []
            # print(f"{interaction.user.display_name} ({user_id}) の通知をクリアしました。")

        except discord.Forbidden:
            await interaction.response.send_message(
                "DMを送信できませんでした。DMがブロックされているか、BotからのDMを許可していません。\n"
                "プライバシー設定で「サーバーにいるメンバーからのダイレクトメッセージを許可する」を有効にしてください。",
                ephemeral=True
            )
            print(f"{interaction.user.display_name} ({user_id}) へのDM送信に失敗しました。")
    else:
        # 通知がない場合
        await interaction.response.send_message("現在、あなたへの新しい通知はありません。", ephemeral=True)
        print(f"{interaction.user.display_name} ({user_id}) に通知がありませんでした。")

# Botを実行
keep_alive()
bot.run(TOKEN)
