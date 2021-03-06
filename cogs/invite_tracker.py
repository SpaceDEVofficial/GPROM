# Copyright: GregTCLTK 2018-2021.
# Contact Developer on https://discord.gg/nPwjaJk (Skidder#8515 | 401817301919465482)
# Cog by: Quill (quillfires)

import discord
import asyncio
import json
import time
import typing
import datetime
from discord.ext import commands
# from discord.ext.commands import has_permissions
from discord import Embed
import asyncpg
import os
import dotenv
dotenv.load_dotenv(verbose=True)
with open('config.json', 'r', encoding='UTF8') as f:
    mydict = json.load(f)

class invite_tracker(commands.Cog):
    """
    Keep track of your invites
    """
    def __init__(self, bot):
        self.bot = bot
        self.version = "1.0.0"
        self.botlog = mydict['bot']['botlog']
        self.prefix = mydict['bot']['prefix']
        self.invites = {}
        bot.loop.create_task(self.load())

    async def load(self):
        await self.bot.wait_until_ready()
        # load the invites
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    def get_category(self,guild):
        members = len(list(filter(lambda x: not x.bot, guild.members)))
        target_category = None
        if members >= 1 and members <= 50:
            target_category = self.bot.get_channel(int(mydict['category']['1-50']))
        elif members >= 51 and members <= 100:
            target_category = self.bot.get_channel(int(mydict['category']['51-100']))
        elif members >= 101 and members <= 200:
            target_category = self.bot.get_channel(int(mydict['category']['101-200']))
        elif members >= 201 and members <= 300:
            target_category = self.bot.get_channel(int(mydict['category']['201-300']))
        elif members >= 301 and members <= 400:
            target_category = self.bot.get_channel(int(mydict['category']['301-400']))
        elif members >= 401 and members <= 500:
            target_category = self.bot.get_channel(int(mydict['category']['401-500']))
        elif members >= 501 and members <= 600:
            target_category = self.bot.get_channel(int(mydict['category']['501-600']))
        elif members >= 601 and members <= 700:
            target_category = self.bot.get_channel(int(mydict['category']['601-700']))
        elif members >= 701 and members <= 800:
            target_category = self.bot.get_channel(int(mydict['category']['701-800']))
        elif members >= 801 and members <= 900:
            target_category = self.bot.get_channel(int(mydict['category']['801-900']))
        elif members >= 901 and members <= 1000:
            target_category = self.bot.get_channel(int(mydict['category']['901-1000']))
        elif members >= 1001:
            target_category = self.bot.get_channel(int(mydict['category']['1001-']))
        return target_category


    @commands.Cog.listener()
    async def on_member_join(self, member):
        pg_con = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PW'),
                                       database=os.getenv('DB_DB'), host=os.getenv('DB_HOST'))
        logchannel = await pg_con.fetchrow("SELECT * FROM invite_conf WHERE guild_id = $1",member.guild.id)
        if not logchannel == None:
            logs = self.bot.get_channel(logchannel[1])
            eme = Embed(description="????????? ?????????????????????.", color=0x03d692, title=" ")
            eme.set_author(name=str(member), icon_url=member.avatar_url)
            eme.set_footer(text="ID: " + str(member.id))
            eme.timestamp = member.joined_at
            try:
                invs_before = self.invites[member.guild.id]
                invs_after = await member.guild.invites()
                self.invites[member.guild.id] = invs_after
                for invite in invs_before:
                    if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                        eme.add_field(name="?????? ??????",
                                      value=f"???????????????: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\n????????????: `{invite.code}`\n????????????: ` {str(int(invite.uses)+1)} `", inline=False)
            except:
                pass
            await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pg_con = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PW'),
                                       database=os.getenv('DB_DB'), host=os.getenv('DB_HOST'))
        logchannel = await pg_con.fetchrow("SELECT * FROM invite_conf WHERE guild_id = $1", member.guild.id)
        if not logchannel == None:
            logs = self.bot.get_channel(logchannel[1])
            eme = Embed(description="???????????? ??????????????????.", color=0xff0000, title=" ")
            eme.set_author(name=str(member), icon_url=member.avatar_url)
            eme.set_footer(text="ID: " + str(member.id))
            eme.timestamp = member.joined_at
            try:
                invs_before = self.invites[member.guild.id]
                invs_after = await member.guild.invites()
                self.invites[member.guild.id] = invs_after
                for invite in invs_before:
                    if invite.uses > self.find_invite_by_code(invs_after, invite.code).uses:
                        eme.add_field(name="?????? ??????",
                                      value=f"???????????????: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\n????????????: `{invite.code}`\n????????????: ` {str(invite.uses)} `", inline=False)
            except:
                pass
            await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
            embed = discord.Embed(colour=discord.Colour.green(), title=":inbox_tray: ?????? ?????? :inbox_tray:")
            embed.add_field(name="?????? ??????", value=f"``{guild.name}``", inline=False)
            embed.add_field(name="?????? ?????????", value=f"``{guild.id}``", inline=False)
            embed.add_field(name="?????? ??????", value=f"``{guild.owner}``", inline=False)
            embed.add_field(name="?????? ????????????", value=f"``{len(list(filter(lambda x: not x.bot, guild.members)))}???``",
                            inline=False)
            embed.add_field(name="?????? ????????? ?????? ???", value=f"``{len(self.bot.guilds)}???`", inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon_url)
            await self.bot.get_channel(int(self.botlog)).send(embed=embed)
            if guild.me.guild_permissions >= discord.Permissions(permissions=8) == False:
                await guild.owner.send(embed=discord.Embed(color=0x7289DA, title="?????? ??????",
                                                           description=f"``{guild.name}`` ???????????? ????????? ????????? ?????????????????????."))
                await guild.leave()
            else:
                text = await guild.create_text_channel(self.bot.user.name)
                omg = await text.send(content=mydict['bot']['guildlink'],
                                      embed=discord.Embed(color=discord.Colour.green(), title=f"{self.bot.user.name} ?????????",
                                                          description=f"{self.bot.user.mention}??? ????????? ??? ??? ?????? ???????????? ????????????.\n\nSTEP 1. ?????? ???????????????. [??? ????????????](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)\nSTEP 2. `{self.bot.get_guild(int(mydict['bot']['guildid'])).name}`??? ????????? ???????????????.\nSTEP 3. `{self.prefix}??????` ???????????? ?????? ???????????? ???????????????.").set_footer(
                                          text="??????????????? ????????? - https://github.com/samsunghappytree123/makead"))
                await text.edit(topic=f'{omg.id}')
                await text.set_permissions(guild.default_role, read_messages=True, send_messages=False,
                                           read_message_history=True)
                await text.set_permissions(self.bot.user, read_messages=True, send_messages=True,
                                           read_message_history=True)
                target_category = self.get_category(guild)
                serverchannel = await target_category.create_text_channel(guild.name)
                url = await text.create_invite(reason=f'{self.bot.user.name}')
                m = await serverchannel.send(f"{url}",
                                             embed=discord.Embed(colour=discord.Colour.green(), title=guild.name,
                                                                 description=f"?????? ????????? ????????????.\n``{self.prefix}??????`` ???????????? ????????? ??????????????????.").set_footer(
                                                 text="??????????????? ????????? - https://github.com/samsunghappytree123/makead"))
                await serverchannel.edit(topic=f'{guild.id} {m.id} {text.id}')
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
            embed = discord.Embed(colour=discord.Colour.red(), title=":outbox_tray: ?????? ?????? :outbox_tray:")
            embed.add_field(name="?????? ??????", value=f"``{guild.name}``", inline=False)
            embed.add_field(name="?????? ?????????", value=f"``{guild.id}``", inline=False)
            embed.add_field(name="?????? ??????", value=f"``{guild.owner}``", inline=False)
            embed.add_field(name="?????? ????????????", value=f"``{len(list(filter(lambda x: not x.bot, guild.members)))}???``",
                            inline=False)
            embed.add_field(name="?????? ????????? ?????? ???", value=f"``{len(self.bot.guilds)}`???`", inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon_url)
            await self.bot.get_channel(int(self.botlog)).send(embed=embed)
            target_category = self.get_category(guild)
            for a in target_category.channels:
                if str(guild.id) in a.topic:
                    await a.delete()
        except:
            pass


def setup(bot):
    bot.add_cog(invite_tracker(bot))
    print("invite_tracker is loaded!")
