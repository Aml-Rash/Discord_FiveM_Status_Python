import discord
import requests
import random
import datetime
import string
import json
import time
import os
import asyncio
from discord.ext import commands

color = discord.Colour(0x03bafc)
invites = {}
datetime = datetime.datetime.now()
data = {}
lockdown = False
try:
    with open('config.json') as f:
        data = json.load(f)
        configtoken = data["token"]
        configprefix = data["prefix"]
        fivem_server_ip_port = data["fivem_server_ip_port"]
        fivem_server_logo_url = data["fivem_server_logo_url"]
        server_name = data["server_name"]
        cfx_connect_url = data["cfx_connect_url"]
        embed_thumbnail = data["embed_thumbnail"]
        embed_footer = data["embed_footer"]
        moderation_logs = data["moderation_logs"]
        if moderation_logs:
            logs_channel = int(data["logs_channel"])
        welcome_message = data["welcome_message"]
        if welcome_message:
            welcome_channel = int(data["welcome_channel"])
        server_status_data = data["server_status_data"]
        if server_status_data:
            server_status_channel = int(data["server_status_channel"])
except:
    newdata = {}
    newdata["token"] = ""
    newdata["prefix"] = "!"
    newdata["fivem_server_ip_port"] = ""
    newdata["fivem_server_logo_url"] = ""
    newdata["server_name"] = ""
    newdata["cfx_connect_url"] = ""
    newdata["embed_thumbnail"] = ""
    newdata["embed_footer"] = ""
    newdata["moderation_logs"] = False
    newdata["logs_channel"] = ""
    newdata["welcome_message"] = False
    newdata["welcome_channel"] = ""
    newdata["server_status_data"] = False
    newdata["server_status_channel"] = ""

    with open('config.json', 'w') as outfile:
        json.dump(newdata, outfile, indent=2)

    with open('config.json') as f:
        data = json.load(f)
        configtoken = data["token"]
        configprefix = data["prefix"]
        fivem_server_ip_port = data["fivem_server_ip_port"]
        fivem_server_logo_url = data["fivem_server_logo_url"]
        server_name = data["server_name"]
        cfx_connect_url = data["cfx_connect_url"]
        embed_thumbnail = data["embed_thumbnail"]
        embed_footer = data["embed_footer"]
        moderation_logs = data["moderation_logs"]
        if moderation_logs:
            logs_channel = int(data["logs_channel"])
        welcome_message = data["welcome_message"]
        if welcome_message:
            welcome_channel = int(data["welcome_channel"])
        server_status_data = data["server_status_data"]
        if server_status_data:
            server_status_channel = int(data["server_status_channel"])

bot = commands.Bot(command_prefix = configprefix)
bot.remove_command('help')

embed_footer = f'{embed_footer} | Made by Aml#8966'
'''@bot.event
async def on_command_error(ctx, error):
    from discord.ext.commands import CommandNotFound
    from discord.ext.commands import MissingRequiredArgument
    from discord.ext.commands import BadArgument
    if isinstance(error, MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send('Missing required arguments.')
    elif isinstance(error, BadArgument):
        await ctx.message.delete()
        await ctx.send('Bad argument provided.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("You dont have permissions to perform this action.")
    elif isinstance(error, CommandNotFound):
        await ctx.message.delete()
        await ctx.send('I dont recognize that command.')
    else:
        print(error)'''

async def loop1():
    randomcolors = [0x03bafc, 0x16f7e8, 0x34f716, 0xff0800, 0xff0800, 0x8400ff, 0xff003c]
    if server_status_data:
        print('\x1b[32mSetting up bot....\x1b0m')
        fivem_status_channel = bot.get_channel(server_status_channel)
        await fivem_status_channel.purge(limit=200)
        altcolor = discord.Colour(random.choice(randomcolors))
        usernames = []
        try:
            res = requests.get(f'http://{fivem_server_ip_port}/dynamic.json')
            data = res.json()
            res3 = requests.get(f'http://{fivem_server_ip_port}/players.json')
            data3 = res3.json()
            for name in data3:
                usernames.append(name["name"])
            if len(str(data3)) > 3:
                usernames = '\n'.join('{}' for _ in range(len(usernames))).format(*usernames)
            if str(data3) == '[]':
                usernames = 'No players online'
            embed = discord.Embed(title=f'{server_name} is currently Online', color=altcolor)
            embed.add_field(name='How to join the server?', value=f'1. You can join the server using the F8 Console by typing `connect {cfx_connect_url}`\n2. Or just by searching `{server_name}` in the FiveM server list.', inline=False)
            embed.add_field(name='Server Status', value=':white_check_mark: Online')
            embed.add_field(name='Online Players', value=str(data["clients"]) + '/' + data["sv_maxclients"])
            embed.add_field(name='Player List', value=usernames, inline=False)
            embed.set_thumbnail(url=fivem_server_logo_url)
            embed.set_footer(text=embed_footer)
            message = await fivem_status_channel.send(embed=embed)
            os.system('cls')
            print('Bot is up')
        except:
            errorembed = discord.Embed(title=f'{server_name} is currently Offline', color=color)
            await fivem_status_channel.send(embed=errorembed)
            activity = discord.Game(name=f"Server Offline", type=3)
            await bot.change_presence(activity=activity)
            os.system('cls')
            print('Bot is up')
            print('Server is detected offline, for the live playercount to work you will have to restart the bot whenever the server is online.')
            return
        while True:
            altcolor = discord.Colour(random.choice(randomcolors))
            usernames = []
            res = requests.get(f'http://{fivem_server_ip_port}/dynamic.json')
            data = res.json()
            res3 = requests.get(f'http://{fivem_server_ip_port}/players.json')
            data3 = res3.json()
            playercount = str(data["clients"]) + '/' + str(data["sv_maxclients"])
            activity = discord.Activity(name=f"{playercount} players", type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity)
            for name in data3:
                usernames.append(name["name"])
            if len(str(data3)) > 3:
                usernames = '\n'.join('{}' for _ in range(len(usernames))).format(*usernames)
            if str(data3) == '[]':
                usernames = 'No players online'
            new_embed = discord.Embed(title=f'{server_name} is currently Online', color=altcolor,
            description=f'**How to join the server?**\n1. You can join the server using the F8 Console by typing `connect {cfx_connect_url}`\n2. Or just by searching `{server_name}` in the FiveM server list.')
            new_embed.add_field(name='\nServer Status', value=':white_check_mark: Online')
            new_embed.add_field(name='Online Players', value=str(data["clients"]) + '/' + data["sv_maxclients"])
            new_embed.add_field(name='\nPlayer List', value=usernames, inline=False)
            new_embed.set_thumbnail(url=fivem_server_logo_url)
            new_embed.set_footer(text=embed_footer)
            await message.edit(embed=new_embed)
            await asyncio.sleep(5)
    else:
        print(f'The bot is up in {len(bot.guilds)} server/s')

@bot.event
async def on_connect():
    for guild in bot.guilds:
        invites[guild.id] = await guild.invites()
    await loop1()

def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv

@bot.event
async def on_member_join(member):
    global lockdown 
    if lockdown == True:
        member.kick()
    if moderation_logs:
        members = sorted(member.guild.members, key=lambda m: m.joined_at)
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(title='User joined the guild', color=color, timestamp=datetime)
        embed.add_field(name='User', value=member.mention, inline=False)
        embed.add_field(name='User tag', value=member, inline=False)
        embed.add_field(name='User ID', value=member.id, inline=False)
        embed.add_field(name="Join position", value=str(members.index(member)+1), inline=False)
        embed.add_field(name="Joined at", value=member.joined_at.strftime(date_format), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=embed_footer)
        await bot.get_channel(logs_channel).send(embed=embed)
    invites_before_join = invites[member.guild.id]
    invites_after_join = await member.guild.invites()
    if welcome_message:
        for invite in invites_before_join:
            if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
                invites[member.guild.id] = invites_after_join
                embed = discord.Embed(title='Welcome',
                description=f'Welcome to the Discord server, {member.mention}\n\nInvited by: {invite.inviter}',
                color=color, timestamp=datetime)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=embed_footer)
                await bot.get_channel(welcome_channel).send(embed=embed)
                return
            else:
                embed = discord.Embed(title='Welcome',
                description=f'Welcome to the Discord server, {member.mention}\n\nInvited by: Uknown',
                color=color)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=embed_footer)
                await bot.get_channel(welcome_channel).send(embed=embed)
                return

@bot.event
async def on_member_remove(member):
    if moderation_logs:
        members = sorted(member.guild.members, key=lambda m: m.joined_at)
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(title='User left the guild', color=color, timestamp=datetime)
        embed.add_field(name='User', value=member.mention, inline=False)
        embed.add_field(name='User tag', value=member, inline=False)
        embed.add_field(name="Joined at", value=member.joined_at.strftime(date_format), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=embed_footer)
        await bot.get_channel(logs_channel).send(embed=embed)
    
@bot.event
async def on_message_delete(ctx):
    if moderation_logs and not ctx.author.bot:
        embed = discord.Embed(title='Message Deleted', color=color, timestamp=datetime)
        embed.add_field(name='Message author', value=f'<@{ctx.author.id}>', inline=False)
        embed.add_field(name='Message author tag', value=ctx.author, inline=False)
        embed.add_field(name='Message author ID', value=ctx.author.id, inline=False)
        embed.add_field(name='Message content', value=ctx.content, inline=False)
        embed.set_footer(text=embed_footer)
        await bot.get_channel(logs_channel).send(embed=embed)

@bot.command(name='ping')
async def _ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'Pong! **{round(bot.latency * 1000)}ms**')

@bot.command(name='ban')
@commands.has_permissions(ban_members = True)
async def _ban(ctx, user: discord.Member=None, *, reason=None):
    if user == None:
        await ctx.send('You need to provide a user to ban.')
        return
    if reason == None:
        reason = 'N/A'
    await user.ban()
    message = f'You have been banned from {ctx.guild.name} for the following reason/s: {reason}'
    try:
        await user.send(message)
    except:
        print('I couldn\'t send a dm to a user because they have their dms locked')
        pass
    embed = discord.Embed(title='User banned from the guild', color=color, timestamp=datetime)
    embed.add_field(name='User banned', value=user.mention)
    embed.add_field(name='Banned by', value=ctx.author.mention)
    embed.add_field(name='Reason', value=reason, inline=False)
    embed.set_thumbnail(url=embed_thumbnail)
    embed.set_footer(text=embed_footer)
    message = await ctx.channel.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@bot.command(name='kick')
@commands.has_permissions(kick_members = True)
async def _kick(ctx, user: discord.Member=None):
    if user == None:
        await ctx.send('You need to provide a user to kick.')
        return
    await user.kick()
    embed = discord.Embed(title='User kicked from the guild', color=color, timestamp=datetime)
    embed.add_field(name='User kicked', value=user.mention)
    embed.add_field(name='Kicked by', value=ctx.author.mention)
    embed.set_thumbnail(url=embed_thumbnail)
    embed.set_footer(text=embed_footer)
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@bot.command(name='purge')
@commands.has_permissions(manage_messages = True)
async def _purge(ctx, amount:int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title='Channel Purged', description=f'{amount} messages have been purged from this channel.', color=color)
    embed.add_field(name='Purged By', value=f'<@{ctx.author.id}>')
    embed.set_footer(text=embed_footer)
    message = await ctx.channel.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

'''@bot.command(name='mute')
@commands.has_permissions(manage_messages = True)
async def _mute(ctx, user:discord.Member=None, time):
    if 's' in time:
        numbers = time
        seconds = list(time)
        time = seconds[:-1]
    elif 'm' in time:

    if user == None:
        await ctx.send('You need to provide a user to mute.')
    muted = discord.utils.get(user.server.roles, name="Muted")
    try:
        await bot.add_roles(user, muted)
    except:
        print('Muted role not found, therefore I cant mute that user.')
        return
    embed = discord.Embed(title='User muted', color=color)
'''

@bot.command()
@commands.has_permissions(manage_messages = True)
async def userinfo(ctx, *, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(description=user.mention, color=color)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text=embed_footer)
    message = await ctx.channel.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@bot.command()
@commands.has_permissions(manage_messages = True)
async def serverinfo(ctx):
    await ctx.message.delete()
    icon_url = ctx.guild.icon_url
    embed = discord.Embed(color=color, timestamp=datetime)
    embed.set_author(name=ctx.guild.name, icon_url=icon_url)
    embed.add_field(name='Owner', value=ctx.guild.owner)
    embed.add_field(name='Region', value=ctx.guild.region)
    embed.add_field(name='Channel Categories', value=len(ctx.guild.categories))
    embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels))
    embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels))
    embed.add_field(name='Members', value=len(ctx.guild.members))
    embed.add_field(name='Roles', value=len(ctx.guild.roles))
    embed.set_footer(text=embed_footer)
    message = await ctx.channel.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@bot.command()
@commands.has_permissions(administrator = True)
async def lockdown(ctx, choice):
    await ctx.message.delete()
    global lockdown
    if choice.lower() == 'on':
        noembed = discord.Embed(title='Server lockdown', description='The server is now in lockdown, anyone that joins the server from now on will be kicked.', color=color, timestamp=datetime)
        noembed.set_footer(text=embed_footer)
        await ctx.send(embed=noembed)
        lockdown = False
    if choice.lower() == 'off':
        noembed = discord.Embed(title='Server lockdown', description='The server is no longer on lockdown, no one will be kicked when joining anymore.', color=color, timestamp=datetime)
        noembed.set_footer(text=embed_footer)
        await ctx.send(embed=noembed)
        lockdown = True
    
try:
    bot.run(configtoken)
except:
    print('The bot token is either none or invalid, please enter a token in the config.json')