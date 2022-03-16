#mainfile

import discord
from discord.ext import commands,tasks
import traceback
import os
import asyncio
from asyncio import sleep
import re
from discord import Permissions
from discord_buttons_plugin import *
from discord import File
from discord import Permissions
from discord.utils import get
from dislash import slash_commands, Option, OptionType
import datetime
import json
import random
from config.server import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.guild_messages = True
with open('config/config.json') as f:
    data = json.load(f)
    prefix = data["prefix"]
client = commands.Bot(command_prefix=prefix,intents=intents)
client.remove_command("help")
slash = slash_commands.SlashClient(client)


@client.event
async def on_ready():
    change_status.start()
    print("discord.py version" + discord.__version__)
    print('We have logged in as {0.user}'.format(client,client))
    while True:
      await asyncio.sleep(5)
      with open("config/antispam.txt", "r+") as file:
        file.truncate(0)


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Streaming(
        name=f"☭discord.py☭", url="https://www.twitch.tv/za_program"))
    await asyncio.sleep(5.0)
    await client.change_presence(activity=discord.Streaming(
        name=
        f"{prefix}help {len(client.guilds)}サーバーと{len(client.users)}人を管理しています",
        url="https://www.twitch.tv/za_program"))
    await asyncio.sleep(5.0)
















@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -MissingPermissions",
                              description=f"実行者の必要な権限が無いため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -BotMissingPermissions",
                              description=f"Botの必要な権限が無いため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title=":x: 失敗 -CommandNotFound",
                              description=f"不明なコマンドもしくは現在使用不可能なコマンドです。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title=":x: 失敗 -MemberNotFound",
                              description=f"指定されたメンバーが見つかりません。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument",
                              description=f"指定された引数がエラーを起こしているため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument",
                              description=f"指定された引数が足りないため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=0x979c9f)
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    else:
        raise error















@client.listen("on_message")
async def stopspam(message):
  if message.channel.topic == "のーぷろてくと":
    return
  if not message.channel.topic == "のーぷろてくと":
   counter = 0
   with open("config/antispam.txt", "r+") as file:
    for lines in file:
      if lines.strip("\n") == str(message.author.id):
        counter+=1
    
    file.writelines(f"{str(message.author.id)}\n")
    if counter > 3:
      await message.channel.purge(limit=5, check=lambda m: m.author==message.author)
      await message.channel.send("stop spam!x5", delete_after=3)
      role = get(message.guild.roles, name="zearamute")
      if not role:
        await message.guild.create_role(name="zearamute")
        role = get(message.guild.roles, name="zearamute")
        await message.author.add_roles(role)
        await asyncio.sleep(3600)
        await message.author.remove_roles(role)
      await message.author.add_roles(role)
      await asyncio.sleep(3600)
      await message.author.remove_roles(role)



  
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=5):
  await ctx.channel.purge(limit=amount)
  await ctx.send("消しました")



global_channel_name = "protectglobal"




@client.listen("on_message")
async def globalchat(message):
    if message.channel.name == global_channel_name:  #グローバルチャットにメッセージが来たとき
        #メッセージ受信部
        if message.author.bot:  #BOTの場合は何もせず終了
            return
        #メッセージ送信部
        for channel in client.get_all_channels():  #BOTが所属する全てのチャンネルをループ
            if channel.name == global_channel_name:  #グローバルチャット用のチャンネルが見つかったとき
                embed = discord.Embed(
                    description=message.content,
                    color=0x979c9f)  #埋め込みの説明に、メッセージを挿入し、埋め込みのカラーを紫`#9B95C9`に設定
                embed.set_author(
                    name="{}#{}".format(message.author.name,
                                        message.author.discriminator),
                    icon_url=
                    "https://media.discordapp.net/avatars/{}/{}.png?size=1024".
                    format(message.author.id, message.author.avatar))
                embed.set_footer(
                    text="{}".format(message.guild.name),
                    icon_url=
                    "https://media.discordapp.net/icons/{}/{}.png?size=1024".
                    format(message.guild.id, message.guild.icon))
                embed.timestamp = datetime.datetime.utcnow()
                if message.attachments != []:  #添付ファイルが存在するとき
                    embed.set_image(url=message.attachments[0].url)

                if message.reference:  #返信メッセージであるとき
                    reference_msg = await message.channel.fetch_message(
                        message.reference.message_id)  #メッセージIDから、元のメッセージを取得
                    if reference_msg.embeds and reference_msg.author == client.user:  #返信の元のメッセージが、埋め込みメッセージかつ、このBOTが送信したメッセージのとき→グローバルチャットの他のサーバーからのメッセージと判断
                        reference_message_content = reference_msg.embeds[
                            0].description  #メッセージの内容を埋め込みから取得
                        reference_message_author = reference_msg.embeds[
                            0].author.name  #メッセージのユーザーを埋め込みから取得
                    elif reference_msg.author != client.user:  #返信の元のメッセージが、このBOTが送信したメッセージでは無い時→同じチャンネルのメッセージと判断
                        reference_message_content = reference_msg.content  #メッセージの内容を取得
                        reference_message_author = reference_msg.author.name + '#' + reference_msg.author.discriminator  #メッセージのユーザーを取得
                    reference_content = ""
                    for string in reference_message_content.splitlines(
                    ):  #埋め込みのメッセージを行で分割してループ
                        reference_content += "> " + string + "\n"  #各行の先頭に`> `をつけて結合
                    reference_value = "**@{}**\n{}".format(
                        reference_message_author,
                        reference_content)  #返信メッセージを生成
                    embed.add_field(name='返信しました',
                                    value=reference_value,
                                    inline=True)  #埋め込みに返信メッセージを追加

                await channel.send(embed=embed)  #メッセージを送信
                await asyncio.sleep(2)
                await message.delete()

















@client.event
async def on_guild_join(guild):
    await guild.guild.create_role(name="zearamute")
    embed = discord.Embed(title="サーバーフリーズプロテクター",description="""prefixはsfp!!です！！！
slashコマンドもありますよ！α版なので少ししか機能がないです
webサイトは[こちらです]()

""",color=0x979c9f)
    await guild.system_channel.send(embed=embed)



@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx,user:discord.Member,reason,time):
  if not user:
    await ctx.send("userが選択されてないです\n```sfp!mute discord#1234 spam 100```")
   if not reason:
    role = get(message.guild.roles, name="zearamute")
    await user.add_roles(role)
    await asyncio.sleep(time)
    await user.remove_roles(role,reason="時間が来たから")
  if not time:
    role = get(message.guild.roles, name="zearamute")
    await user.add_roles(role,reason=reason)
  role = get(message.guild.roles, name="zearamute")
  await user.add_roles(role,reason=reason)
  await asyncio.sleep(time)
  await user.remove_roles(role,reason="時間が来たから")

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx,user:discord.Member,reason):
  if not user:
    await ctx.send("userが選択されてないです\n```sfp!unmute discord#1234 時間が来たから```")
   if not reason:
    role = get(message.guild.roles, name="zearamute")
    await user.remove_roles(role,reason="時間が来たから")
  role = get(message.guild.roles, name="zearamute")
  await user.remove_roles(role,reason="時間が来たから")

                             # kick ban#
###################################################################################
@client.command()
@commands.has_permissions(manage_roles=True, kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="kick",
                    value=f"起動した人 {ctx.author}\n名前: {user.name}",
                    inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await user.kick(reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def ban(ctx, user: discord.User, *, reason=None):
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="ban",
                    value=f"{ctx.author}がbanしました\n名前: {user.name}",
                    inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await user.ban(reason=reason)
    await ctx.send(embed=embed)
###################################################################################
  
                            #owner#
###################################################################################
@client.command()
@commands.is_owner()
async def gban(ctx, user: discord.User,reason=None):
    for guild in client.guilds:
        await guild.ban(user,reason=reason)
        await asyncio.sleep(5)
    await ctx.send(f"{user} banned")
    await ctx.send(f"banしたserver数{len(client.guilds)}")


@client.command()
@commands.is_owner()
async def gunban(ctx, user: discord.User, reason=None):
    for guild in client.guilds:
        await guild.unban(user,reason=reason)
        await asyncio.sleep(5)
    await ctx.send(f"{user} unbanned")
    await ctx.send(f"unbanしたserver数{len(client.guilds)}")




@client.command()
@commands.is_owner()
async def eval(ctx, *, code):
    language_specifiers = [
        "python", "py", "javascript", "js", "html", "css", "php", "md",
        "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp",
        "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee",
        "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql",
        "swift", "vim", "xml", "yaml"
    ]
    loops = 0
    while code.startswith("`"):
        code = "".join(list(code)[1:])
        loops += 1
        if loops == 3:
            loops = 0
            break
    for language_specifier in language_specifiers:
        if code.startswith(language_specifier):
            code = code.lstrip(language_specifier)
    while code.endswith("`"):
        code = "".join(list(code)[0:-1])
        loops += 1
        if loops == 3:
            break
    code = "\n".join(
        f"    {i}"
        for i in code.splitlines())  #Adds an extra layer of indentation
    code = f"async def eval_expr():\n{code}"  #Wraps the code inside an async function

    def send(
        text
    ):  #Function for sending message to discord if code has any usage of print function
        client.loop.create_task(ctx.send(text))

    env = {
        " ": " ",
        """
        """: "\n",
        "bot": client,
        "client": client,
        "ctx": ctx,
        "send": send,
        "print": send,
        "_author": ctx.author,
        "_message": ctx.message,
        "_channel": ctx.channel,
        "_guild": ctx.guild,
        "_me": ctx.me,
        "console.log": send
    }
    env.update(globals())
    try:
        exec(code, env)
        eval_expr = env["eval_expr"]
        result = await eval_expr()
        if result:
            embed = discord.Embed(title="result" + "\n",
                                  description=f"```{result}```",
                                  color=0x979c9f)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="error" + "\n",
                              description=f"```{traceback.format_exc()}```",
                              color=0x979c9f)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


client.load_extension('jishaku')
####################################################################################

                             #badword#
####################################################################################




with open('config/badwords.txt','r') as f:
    bad_words = '|'.join(s for l in f for s in l.split(', '))
    bad_word_checker = re.compile(bad_words).search

@client.listen("on_message")
async def badword(message):
    if bad_word_checker(message.content):
        await message.channel.send(f"{message.author.mention}\nngword❌", delete_after=4)
        await message.delete()
        await message.channel.send("deleted", delete_after=4)
        await message.channel.send("ngwordなので送らないでください",delete_after=4)
####################################################################################
  


                                #slash#
###################################################################################



@slash.command(
    name = 'help',
    description = 'helpコマンドです',
    options = [
        Option('command', 'コマンド名', OptionType.STRING),
    ]
)
async def help(ctx,*, command=None):
  if not command:
    embed = discord.Embed(title="コマンド一覧",color=0x979c9f)
    embed.add_field(name="詳細",value="```sc!help <cmd>で詳しくコマンドの説明を見れます\nチャンネルのトピックに<のーせきゅりてぃ>と入力するとセキュリティを無くせます👍```")
    embed.add_field(name="一般",value="```wiki join leave stop```",inline=False)
    embed.add_field(name="security",value="```kick,ban```",inline=False)
    embed.add_field(name="owner",value="```gban gunban eval jsk```",inline=False)
    embed.add_field(name="message manage", value="```10秒間に5回メッセージを送信するとメッセージが削除されます\nngwordを送ると消されます```", inline=False)
    await ctx.send(embed=embed)
  if command == "kick":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="kickコマンド",value="```sc!#kick <user#1234> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if command == "ban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="banコマンド",value="```sc!ban <user#1234> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if command == "wiki":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="wikiコマンド",value="```sc!wiki <word>```",inline=False)
    await ctx.send(embed=embed)
  if command == "join":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="joinコマンド",value="```sc!join```",inline=False)
    await ctx.send(embed=embed)
  if command == "leave":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="leaveコマンド",value="```sc!leave```",inline=False)
    await ctx.send(embed=embed)
  if command == "stop":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="コマンド",value="```sc!stop```",inline=False)
    await ctx.send(embed=embed)
  if command == "gban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="gbanコマンド",value="```sc!gban <user> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if command == "gunban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="gunbanコマンド",value="```sc!gunban <user> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if command == "eval":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="evalコマンド",value="```sc!eval <code>```",inline=False)
    await ctx.send(embed=embed)
  if command == "jsk":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="jskコマンド",value="```sc!jsk <code>```",inline=False)
    await ctx.send(embed=embed)

  
      
###################################################################################




@client.command()
async def help(ctx,*, args=None):
  if not args:
    embed = discord.Embed(title="コマンド一覧",color=0x979c9f)
    embed.add_field(name="詳細",value="```sc!help <cmd>で詳しくコマンドの説明を見れます\nチャンネルのトピックに<のーせきゅりてぃ>と入力するとセキュリティを無くせます👍```")
    embed.add_field(name="一般",value="```wiki```",inline=False)
    embed.add_field(name="security",value="```kick,ban```",inline=False)
    embed.add_field(name="owner",value="```gban gunban eval jsk```",inline=False)
    embed.add_field(name="message manage", value="```10秒間に5回メッセージを送信するとメッセージが削除されます\nngwordを送ると消されます```", inline=False)
    await ctx.send(embed=embed)
  if args == "kick":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="kickコマンド",value="```sc!#kick <user#1234> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if args == "ban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="banコマンド",value="```sc!ban <user#1234> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if args == "wiki":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="wikiコマンド",value="```sc!wiki <word>```",inline=False)
    await ctx.send(embed=embed)
  if args == "gban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="gbanコマンド",value="```sc!gban <user> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if args == "gunban":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="gunbanコマンド",value="```sc!gunban <user> <reason>```",inline=False)
    await ctx.send(embed=embed)
  if args == "eval":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="evalコマンド",value="```sc!eval <code>```",inline=False)
    await ctx.send(embed=embed)
  if args == "jsk":
    embed = discord.Embed(color=0x979c9f)
    embed.add_field(name="jskコマンド",value="```sc!jsk <code>```",inline=False)
    await ctx.send(embed=embed)














keep_alive()


client.run(os.getenv("TOKEN"),bot=True)
