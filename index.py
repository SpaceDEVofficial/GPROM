# coding=utf-8

import discord, asyncio, os, math, ast, datetime, json, dotenv, random, traceback
from discord.ext import commands
import asyncpg
dotenv.load_dotenv(verbose=True)
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members=True
client = commands.Bot(intents=intents,command_prefix="gp!")

with open('config.json', 'r', encoding='UTF8') as f:
    mydict = json.load(f)

prefix = mydict['bot']['prefix']
owner = mydict['bot']['owners']
guildpass = mydict['bot']['guildpass']
botlog = mydict['bot']['botlog']
nameprefix = mydict['bot']['nameprefix']
cooltime2 = []
cooltime_up = []

def get_category(guild):
    members = len(list(filter(lambda x: not x.bot, guild.members)))
    target_category = None
    if members >= 1 and members <= 50:
        target_category = client.get_channel(int(mydict['category']['1-50']))
    elif members >= 51 and members <= 100:
        target_category = client.get_channel(int(mydict['category']['51-100']))
    elif members >= 101 and members <= 200:
        target_category = client.get_channel(int(mydict['category']['101-200']))
    elif members >= 201 and members <= 300:
        target_category = client.get_channel(int(mydict['category']['201-300']))
    elif members >= 301 and members <= 400:
        target_category = client.get_channel(int(mydict['category']['301-400']))
    elif members >= 401 and members <= 500:
        target_category = client.get_channel(int(mydict['category']['401-500']))
    elif members >= 501 and members <= 600:
        target_category = client.get_channel(int(mydict['category']['501-600']))
    elif members >= 601 and members <= 700:
        target_category = client.get_channel(int(mydict['category']['601-700']))
    elif members >= 701 and members <= 800:
        target_category = client.get_channel(int(mydict['category']['701-800']))
    elif members >= 801 and members <= 900:
        target_category = client.get_channel(int(mydict['category']['801-900']))
    elif members >= 901 and members <= 1000:
        target_category = client.get_channel(int(mydict['category']['901-1000']))
    elif members >= 1001:
        target_category = client.get_channel(int(mydict['category']['1001-']))
    return target_category

@client.event
async def bg_change_playing():
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{mydict['bot']['prefix']}가이드 | {len(client.guilds)}개 서버 홍보중"))
        await client.get_channel(int(mydict['category']['1-50'])).edit(name=f"👥 1~50명 ({len(client.get_channel(int(mydict['category']['1-50'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['51-100'])).edit(name=f"👥 51~100명 ({len(client.get_channel(int(mydict['category']['51-100'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['101-200'])).edit(name=f"👥 101~200명 ({len(client.get_channel(int(mydict['category']['101-200'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['201-300'])).edit(name=f"👥 201~300명 ({len(client.get_channel(int(mydict['category']['201-300'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['301-400'])).edit(name=f"👥 301~400명 ({len(client.get_channel(int(mydict['category']['301-400'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['401-500'])).edit(name=f"👥 401~500명 ({len(client.get_channel(int(mydict['category']['401-500'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['501-600'])).edit(name=f"👥 501~600명 ({len(client.get_channel(int(mydict['category']['501-600'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['601-700'])).edit(name=f"👥 601~700명 ({len(client.get_channel(int(mydict['category']['601-700'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['701-800'])).edit(name=f"👥 701~800명 ({len(client.get_channel(int(mydict['category']['701-800'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['801-900'])).edit(name=f"👥 801~900명 ({len(client.get_channel(int(mydict['category']['801-900'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['901-1000'])).edit(name=f"👥 901~1000명 ({len(client.get_channel(int(mydict['category']['901-1000'])).channels)}개 서버 홍보중)")
        await client.get_channel(int(mydict['category']['1001-'])).edit(name=f"👥 1001명 이상 ({len(client.get_channel(int(mydict['category']['1001-'])).channels)}개 서버 홍보중)")
        await asyncio.sleep(300)
    client.loop.create_task(bg_change_playing())


def AutoCogs(client):
    os = __import__("os")
    cog_list = os.listdir("cogs/")
    cog_list = [cog for cog in cog_list if cog.endswith(".py")]
    for i in cog_list:
        cog_name = "cogs." + i.replace(".py", "")
        client.load_extension(cog_name)

@client.event
async def on_ready():
    AutoCogs(client)
    print(f"{client.user.name}이 준비됨!")
    embed = discord.Embed(colour=discord.Colour.purple(), title="🚦 봇 켜짐 🚦")
    embed.add_field(name="전체 서버 수", value=f"`{len(client.guilds)}개`", inline=False)
    embed.add_field(name="전체 인원 수", value=f"`{len(client.users)}명`", inline=False)
    embed.set_footer(text=client.user, icon_url=client.user.avatar_url)
    await client.get_channel(int(botlog)).send(embed=embed)
    client.loop.create_task(bg_change_playing())
    client.loop.create_task(synchronization())

@client.event
async def synchronization():
    c = [
        int(mydict['category']['1-50']),
        int(mydict['category']['51-100']),
        int(mydict['category']['101-200']),
        int(mydict['category']['201-300']),
        int(mydict['category']['301-400']),
        int(mydict['category']['401-500']),
        int(mydict['category']['501-600']),
        int(mydict['category']['601-700']),
        int(mydict['category']['701-800']),
        int(mydict['category']['801-900']),
        int(mydict['category']['901-1000']),
        int(mydict['category']['1001-'])
    ]
    number = 0
    ab = []
    for a in c:
        for i in client.get_channel(int(a)).channels:
            try:
                guild = client.get_guild(int(i.topic.split(" ")[0]))
                members = len(list(filter(lambda x: not x.bot,guild.members)))
                try:
                    if not str(client.get_channel(int(i.topic.split(" ")[2]))) == "None":
                        try:
                            if guild.me.guild_permissions >= discord.Permissions(permissions=8) == False:
                                await guild.owner.send(embed=discord.Embed(color=0x7289DA, title="퇴장 안내", description=f"``{guild.name}`` 서버에서 권한이 부족해 퇴장하였습니다.").set_footer(text="오픈소스를 사용함 - https://github.com/samsunghappytree123/makead"))
                                await guild.leave()
                            else:
                                asdf = client.get_channel(int(i.topic.split(" ")[2]))
                                tg = await asdf.fetch_message(int(asdf.topic.split(" ")[0]))
                                await tg.edit(content=f"<a:loading:774533173722873856> `{client.get_guild(int(mydict['bot']['guildid'])).name}` 서버와 동기화중입니다.", embed=None)
                                await asyncio.sleep(1)
                                embed=discord.Embed(timestamp=tg.edited_at, color=discord.Colour.green(), title=f"{client.user.name} 사용법", description=f"{client.user.mention}은 홍보를 할 수 있는 디스코드 봇입니다.\n\nSTEP 1. 봇을 초대합니다. [봇 초대링크](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)\nSTEP 2. `{client.get_guild(int(mydict['bot']['guildid'])).name}`에 채널이 생성됩니다.\nSTEP 3. `{prefix}등록` 명령어로 서버 명령어를 등록합니다.")
                                embed.set_footer(text="마지막 동기화, 오픈소스를 사용함 - https://github.com/samsunghappytree123/makead")
                                await tg.edit(content=mydict['bot']['guildlink'],embed=embed)
                                target_category = None
                                if members >= 1 and members <= 50:
                                    target_category = client.get_channel(int(mydict['category']['1-50']))
                                elif members >= 51 and members <= 100:
                                    target_category = client.get_channel(int(mydict['category']['51-100']))
                                elif members >= 101 and members <= 200:
                                    target_category = client.get_channel(int(mydict['category']['101-200']))
                                elif members >= 201 and members <= 300:
                                    target_category = client.get_channel(int(mydict['category']['201-300']))
                                elif members >= 301 and members <= 400:
                                    target_category = client.get_channel(int(mydict['category']['301-400']))
                                elif members >= 401 and members <= 500:
                                    target_category = client.get_channel(int(mydict['category']['401-500']))
                                elif members >= 501 and members <= 600:
                                    target_category = client.get_channel(int(mydict['category']['501-600']))
                                elif members >= 601 and members <= 700:
                                    target_category = client.get_channel(int(mydict['category']['601-700']))
                                elif members >= 701 and members <= 800:
                                    target_category = client.get_channel(int(mydict['category']['701-800']))
                                elif members >= 801 and members <= 900:
                                    target_category = client.get_channel(int(mydict['category']['801-900']))
                                elif members >= 901 and members <= 1000:
                                    target_category = client.get_channel(int(mydict['category']['901-1000']))
                                elif members >= 1001:
                                    target_category = client.get_channel(int(mydict['category']['1001-']))
                                await i.edit(name=guild.name, category=target_category)
                                number += 1
                                ab.append(guild.id)
                        except: await client.get_channel(int(botlog)).send(embed=discord.Embed(title="동기화 오류 발생.", colour=discord.Colour.red(), description=f"{guild.name} / {guild.owner} / {guild.id}").set_footer(text=guild.name, icon_url=guild.icon_url))
                except: await client.get_channel(int(botlog)).send(embed=discord.Embed(title="동기화 오류 발생.", colour=discord.Colour.red(), description=f"{guild.name} / {guild.owner} / {guild.id}").set_footer(text=guild.name, icon_url=guild.icon_url))
            except:
                await i.delete()
    abc = []
    for i in client.guilds:
        if not i.id in ab:
            if not i.id in guildpass:
                abc.append(i.id)
    await client.get_channel(int(botlog)).send(embed=discord.Embed(color=0x7289DA, title="🔁 동기화 알림", description=f"{client.user.name} 봇이 접속한 {len(client.guilds)-len(guildpass)}개의 서버 중 {number}개의 서버에 동기화를 완료했으며, {len(client.guilds)-len(guildpass)-number}개의 서버에 동기화를 실패하였습니다."))
    if not len(abc) == 0:
        await client.get_channel(int(botlog)).send(embed=discord.Embed(colour=discord.Colour.red(), title="🔁 동기화 실패 서버 안내", description=f"{abc}"))
        for i in abc:
            guild = client.get_guild(i)
            embed=discord.Embed(color=0x7289DA, title="퇴장 알림", description=f"안녕하세요? ``{guild.name}`` 서버장님! {client.user.name}에서 안내드립니다.\n{client.user.name}에서는 1시간에 1번 동기화를 진행하고 있습니다!\n하지만 동기화 중, ``{guild.name}`` 서버의 동기화가 실패되어 퇴장하였습니다.\n봇이 퇴장한 후에도 아래의 링크로 봇을 다시 초대하실 수 있습니다!")
            embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
            embed.add_field(name="봇 초대 링크", value=f"[봇 초대하기](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)", inline=False)
            embed.add_field(name="서버 초대 링크", value=f"[{mydict['bot']['guildlink']}]({mydict['bot']['guildlink']})", inline=False)
            embed.set_footer(text="오픈소스를 사용함 - https://github.com/samsunghappytree123/makead")
            try: await guild.owner.send(embed=embed)
            except: pass
            await guild.leave()
    await asyncio.sleep(3600)
    client.loop.create_task(synchronization())

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)





@client.event
async def on_message(message):
    if message.content.startswith(f"{prefix}eval"):
        if message.author.id in owner:
            try:
                prefix_count=len(prefix)+5
                cmd=message.content[prefix_count:]
                fn_name = "_eval_expr"
                cmd = cmd.strip("` ")
                # add a layer of indentation
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                # wrap in async def body
                body = f"async def {fn_name}():\n{cmd}"
                parsed = ast.parse(body)
                body = parsed.body[0].body
                insert_returns(body)
                env = {
                    'client': client,
                    'discord': discord,
                    'message': message,
                    '__import__': __import__
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)
                result = (await eval(f"{fn_name}()", env))
                embed=discord.Embed(title="실행 성공", colour=discord.Colour.green(), timestamp=message.created_at)
                embed.add_field(name="`📥 Input (들어가는 내용) 📥`", value=f"```py\n{cmd}```", inline=False)
                embed.add_field(name="`📤 Output (나오는 내용) 📤`", value=f"```py\n{result}```", inline=False)
                embed.add_field(name="`🔧 Type (타입) 🔧`",value=f"```py\n{type(result)}```", inline=False)
                embed.add_field(name="`🏓 Latency (지연시간) 🏓`",value=f"```py\n{str((datetime.datetime.now()-message.created_at)*1000).split(':')[2]}```", inline=False)
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            except Exception as e:
                await message.channel.send(f"{message.author.mention}, 실행 중 오류가 발생하였습니다.\n\n```py\n{e}```")
        else:
            await message.channel.send(f"{message.author.mention}, 당신은 권한이 없습니다.")

    if message.content == f"{prefix}가이드":
        await message.channel.send(message.author.mention, embed=discord.Embed(color=discord.Colour.green(), title=f"{client.user.name} 사용법", description=f"{client.user.mention}은 홍보를 할 수 있는 디스코드 봇입니다.\n\nSTEP 1. 봇을 초대합니다. [봇 초대링크](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)\nSTEP 2. `{client.get_guild(int(mydict['bot']['guildid'])).name}`에 채널이 생성됩니다.\nSTEP 3. `{prefix}등록` 명령어로 서버 명령어를 등록합니다.").set_footer(text="오픈소스를 사용함 - https://github.com/samsunghappytree123/makead"))

    if message.content.startswith(f"{prefix}등록"):
        if message.author.guild_permissions.administrator == True:
            if message.guild.id in cooltime2:
                await message.channel.send(f"{message.author.mention}, 쿨타임이 적용되어 있습니다. 기다려주세요.")
            else:
                cmd = message.content[len(prefix)+3:]
                if cmd == "" or cmd == " ":
                    await message.channel.send(f"{message.author.mention}, 서버 소개 내용 `{prefix}등록` 커맨드와 함께 써주세요.")
                else:
                    msg = await message.channel.send(f"<a:loading:774533173722873856> {message.author.mention}, `{message.guild.name}` 서버의 설명을 포스트중입니다...")
                    target_category = get_category(message.guild)
                    for a in target_category.channels:
                        splits = a.topic.split(" ")
                        if str(message.guild.id) == splits[0]:
                            m = await a.fetch_message(int(splits[1]))
                            embed=discord.Embed(colour=discord.Colour.green(), title=message.guild.name, description=cmd).set_footer(text=message.author, icon_url=message.author.avatar_url)
                            if message.guild.is_icon_animated() is True:
                                a = message.guild.icon_url_as(format="gif", size=2048)
                            elif message.guild.is_icon_animated() is False:
                                a = message.guild.icon_url_as(format="png", size=2048)
                            embed.set_thumbnail(url=a)
                            embed.set_footer(text="오픈소스를 사용함 - https://github.com/samsunghappytree123/makead")
                            await m.edit(embed=embed)
                            await msg.edit(content=f"✅ {message.author.mention}, 성공적으로 `{message.guild.name}` 서버의 설명을 포스트하였습니다!")
                            cooltime2.append(message.guild.id)
                            await asyncio.sleep(3600)
                            cooltime2.remove(message.guild.id)
                        else:
                            pass
    if message.content.startswith(f"{prefix}up"):
        if message.author.guild_permissions.administrator == True:
            if message.guild.id in cooltime_up:
                await message.channel.send(f"{message.author.mention}, 쿨타임이 적용되어 있습니다. 기다려주세요.")
            else:
                msg = await message.channel.send(f"<a:loading:774533173722873856> {message.author.mention}, `{message.guild.name}` 서버를 맨위로 올리는 중입니다...")
                target_category = get_category(message.guild)
                for a in target_category.channels:
                    splits = a.topic.split(" ")
                    if str(message.guild.id) == splits[0]:
                        await a.edit(position=0)
                        await msg.edit(content=f"✅ {message.author.mention}, 성공적으로 `{message.guild.name}` 서버를 맨위로 올렸습니다!")
                        cooltime_up.append(message.guild.id)
                        await asyncio.sleep(3600)
                        cooltime_up.remove(message.guild.id)
                    else:
                        pass
    await client.process_commands(message)

@client.command()
async def setlog(ctx,channel:discord.TextChannel=None):
    msg = await ctx.reply("저장중입니다. 잠시만 기다려주세요.")
    pg_con = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PW'),
                                     database=os.getenv('DB_DB'), host=os.getenv('DB_HOST'))
    conf = await pg_con.fetchrow("SELECT * FROM invite_conf WHERE guild_id = $1",ctx.guild.id)
    if channel == None:
        return await msg.edit(content="로그채널을 지정하지 않으셨습니다 `#채널이름`으로 지정해주세요.")
    if conf == None:
        try:
            await pg_con.execute("INSERT INTO invite_conf(guild_id,channel_id) VALUES($1,$2)",ctx.guild.id,channel.id)
            await msg.edit(content="성공적으로 설정되었습니다!")
        except:
            await msg.edit(content="설정을 저장하는도중 에러가 발생해 실패하였습니다. 다시 시도해주세요.")
    else:
        await msg.edit(content=f"이미 등록되어있습니다.\n등록된 채널: <#{conf[1]}>")

@client.command()
async def deletelog(ctx):
    msg = await ctx.reply("삭제중입니다. 잠시만 기다려주세요.")
    pg_con = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PW'),
                                   database=os.getenv('DB_DB'), host=os.getenv('DB_HOST'))
    conf = await pg_con.fetchrow("SELECT * FROM invite_conf WHERE guild_id = $1",ctx.guild.id)
    if conf == None:
        await msg.edit(content=f"등록되어있지 않습니다.`gp!setlog #channelname` 으로 등록해주세요.")
    else:
        try:
            await pg_con.execute("DELETE FROM invite_conf WHERE guild_id=$1",ctx.guild.id)
            await msg.edit(content="성공적으로 삭제되었습니다!")
        except:
            await msg.edit(content="설정을 삭제하는도중 에러가 발생해 실패하였습니다. 다시 시도해주세요.")

client.run(token)
