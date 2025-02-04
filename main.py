# Yes, I am aware that this is open source
# This is supposed to be an exclusive bot
# You can fork and customize, but DO NOT USE THIS TO IMPERSONATE ME

import json
import os

import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions, has_role

token = os.environ['TOKEN']  ## haha no token for you ##

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@client.event
async def on_ready():
  print("Bot is ready")


## CMDS ##
  
@client.command()
async def ping(ctx):
  await ctx.send('Pong!')


@client.command(aliases=['close', 'stop'])
@has_permissions(administrator=True)
async def shutdown(ctx):
  await ctx.send('Shutting down...')
  await client.close()


@client.command(aliases=['execute'])
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='no reason'):
  id = ctx.guild.get_member(member.id)
  await member.ban(reason=reason)
  await ctx.send(f'{member} ({id}) has been executed for {reason}')


@client.command(aliases=['bringeth'])
@has_permissions(ban_members=True)
async def unban(ctx, id: int):
  user = await client.fetch_user(id)
  await ctx.guild.unban(user)
  await ctx.send(f'{user} has been reincarnated.')


@client.command(aliases=['nuke'])
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount)


@client.command(aliases=['arrest'])
@has_permissions(manage_roles=True)
async def jail(ctx, member: discord.Member, *, reason='no reason'):
  await member.add_roles(discord.utils.get(ctx.guild.roles, name='Jailed'))
  await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Verified'))
  await ctx.send(f'{member} has been arrested for {reason}.')


@client.command(aliases=['parole'])
@has_permissions(manage_roles=True)
async def unjail(ctx, member: discord.Member):
  await member.add_roles(discord.utils.get(ctx.guild.roles, name='Verified'))
  await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Jailed'))
  await ctx.send(f'{member} is on parole.')

@client.command(aliases=['exile'])
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason='no reason'):
    await member.kick()
    await ctx.send(f'{member} has been exiled for {reason}')

@client.command(aliases=['gib'])
@has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member} now has the {role} role.')

@client.command(aliases=['ungib'])
@has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'{member} no longer has the {role} role.')

@client.command(aliases=['grantsp'])
@has_role("Developers")
async def givesp(ctx, member: discord.Member):
  data = f'{member}({member.id}) : {ctx.author}'
  jsonFile = open("notedb.json", "w")
  json.dump(f'{member}', jsonFile)
  json.dump(data, jsonFile)
  await ctx.send(f"{member} now has {ctx.author}'s shitping")

@client.command(aliases=['looksp'])
@has_role("Developers")
async def checksp(ctx, member: discord.Member):
  jsonFile = open("notedb.json")
  readData = json.load(jsonFile)
  for i in readData:
    spPerms = i
  await ctx.send(f'{member} has the shitping of the following: {spPerms}')
  


client.run(token)
