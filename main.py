import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# 環境変数からBotのトークンを取得
TOKEN = os.getenv('BOT_TOKEN')

# 必要なインテントを有効にする
# membersインテントはサーバーメンバーの情報を取得するために必要 (通知機能)
# message_contentインテントはメッセージの内容を読み取るために必要 (従来のコマンド用)
intents = discord.Intents.default()
intents.members = True # メンバー情報を取得するために必要
intents.message_content = True # メッセージ内容を読み取るために必要

# Botオブジェクトを作成
# プレフィックス '!' は、もし今後従来のコマンドを追加する際に使用できます。
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

# --- スラッシュコマンド ---

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
    # コマンド実行中に「考え中」を表示し、後で非表示にする (エフェメラル: コマンド実行者のみに見える)
    await interaction.response.defer(ephemeral=True)

    # Botがメッセージを送信できるチャンネル (ここではコマンドが実行されたチャンネル)
    # 実際には、管理者用の特定の通知チャンネルなどに送信することも検討できます
    target_channel = interaction.channel 

    if target_type == "all":
        # 全てのユーザーに通知を送信 (テキストチャンネルへの @everyone メンションとして)
        # DMで全員に送る場合、メンバーをループして送る必要がありますが、レートリミットに注意が必要です。
        # 例:
        # for member in interaction.guild.members:
        #     if not member.bot: # ボットを除外
        #         try:
        #             await member.send(f"管理者からのお知らせ：{message_content}")
        #         except discord.Forbidden:
        #             print(f"{member.display_name} ({member.id}) へのDM送信が禁止されています。")
        
        await target_channel.send(f"@everyone {message_content}")
        await interaction.followup.send("全てのユーザーに通知を送信しました。")
        print(f"全体通知を送信: '{message_content}'")

    elif target_type == "role":
        if not role_name:
            await interaction.followup.send("ロール名を指定してください。例: `/notification role:管理者 message_content:重要な連絡です`")
            return

        # ロール名からロールオブジェクトを取得
        target_role = discord.utils.get(interaction.guild.roles, name=role_name)

        if target_role:
            # 指定されたロールのメンバーにのみ通知を送信 (ロールをメンション)
            # 特定のロールのメンバーにDMを送る場合の例 (コメントアウトを解除して使用)
            # for member in target_role.members:
            #     if not member.bot:
            #         try:
            #             await member.send(f"{target_role.name}の皆様へ：{message_content}")
            #         except discord.Forbidden:
            #             print(f"{member.display_name} ({member.id}) へのDM送信が禁止されています。")
            
            await target_channel.send(f"{target_role.mention} {message_content}")
            await interaction.followup.send(f"ロール「**{role_name}**」のユーザーに通知を送信しました。")
            print(f"ロール '{role_name}' へ通知を送信: '{message_content}'")
        else:
            await interaction.followup.send(f"ロール「**{role_name}**」が見つかりません。")
            print(f"ロール '{role_name}' が見つかりませんでした。")
    else:
        await interaction.followup.send("無効なターゲットタイプです。「**all**」または「**role**」を指定してください。")
        print("無効なターゲットタイプが指定されました。")

# Botを実行
# 'keep_alive()' はReplitなどの環境でBotを常時稼働させるために使用されます。
# ローカルで実行する場合は不要な場合があります。
keep_alive()
bot.run(TOKEN)
