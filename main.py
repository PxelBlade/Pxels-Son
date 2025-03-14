import json
import os
from dotenv import load_dotenv

import time

import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands.core import has_permissions, has_role
import discord.utils
from discord.utils import get

#Replace with your own server's ID
serverID = 928008543305629768

#TEMPLATES FOR FILEPATH:
#("Folder" is there to show you how to add a folder to the path)
#Windows: C:\Folder\token.env
#Linux & Mac: ~/Folder/token.env
load_dotenv(dotenv_path="~/token.env")

token = os.getenv("TOKEN")
if token:
  print("Token found")

intents = discord.Intents.all()
client = commands.Bot()


@client.event
async def on_ready():
  print("Bot is ready")
  


## CMDS ##
  
@client.slash_command(
name="ping",
description="Check the bot's latency",
guild_ids=[serverID]
)
async def ping(ctx):
  await ctx.respond(f"Pong! ({round(client.latency * 1000)}ms)")

@client.slash_command(
  name="execute",
  description="Ban a user",
  guild_ids=[serverID]
)
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.create_dm()
  await user.send(f"You have been banned from {ctx.guild.name}. Reason: {reason}")
  await user.ban(reason=reason)
  await ctx.respond(f"{user} has been banned")

@client.slash_command(
  name="dm",
  description="DM a user",
  guild_ids=[serverID]
)
@has_role("Developers")
async def dm(ctx, user: discord.Member, *, message):
  await user.send(message)
  await ctx.respond(f"Sent message to {user}")

@client.slash_command(
  name="purge",
  description="Delete messages",
  guild_ids=[serverID]
)
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount)
  await ctx.respond(f"Deleted {amount} messages")
  time.sleep(3)
  await ctx.channel.purge(limit=1)

@client.slash_command(
  name="revive",
  description="Unban a user",
  guild_ids=[serverID]
)
@has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
  await ctx.guild.unban(user)
  await ctx.respond(f"Revived {user}")

@client.slash_command(
  name="exile",
  description="Kick a user",
  guild_ids=[serverID]
)
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.create_dm()
  await user.send(f"You have been kicked from {ctx.guild.name}. Reason: {reason}")
  await user.kick(reason=reason)
  await ctx.respond(f"{user} has been kicked")

@client.slash_command(
  name="gib",
  description="Add a role to a user",
  guild_ids=[serverID]
)
@has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
  if user.top_role.position > ctx.author.top_role.position:
    await ctx.respond("You cannot add a role higher than or equal to your own")
  await user.add_roles(role)
  await ctx.respond(f"Added {role} to {user}")

@client.slash_command(
  name="ungib",
  description="Remove a role from a user",
  guild_ids=[serverID]
)
@has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
  if user.top_role.position > ctx.author.top_role.position:
    await ctx.respond("You cannot remove a role higher than or equal to your own")
  await user.remove_roles(role)
  await ctx.respond(f"Removed {role} from {user}")

@client.slash_command(
  name="arrest",
  description="Arrest a user",
  guild_ids=[serverID]
)
@has_permissions(manage_roles=True)
async def arrest(ctx, user: discord.Member):
  if ctx.author.top_role.position <= user.top_role.position:
    await ctx.respond("You cannot arrest a user with a role higher than or equal to than you")
  guild = user.guild
  sRoles = guild.roles
  for i in sRoles:
    if i == "Jailed":
      jailed = i
      break
  await user.edit(roles=[])
  await user.add_roles(jailed)
  await user.move_to(None) #Kicks from VC (This is the only thing I find confusing to code)
  await ctx.respond(f"{user} has been arrested")

@client.slash_command(
  name="parole",
  description="Parole a user",
  guild_ids=[serverID]
)
@has_permissions(manage_roles=True)
async def parole(ctx, user: discord.Member):
  if ctx.author.top_role.position <= user.top_role.position:
    await ctx.respond("You cannot arrest a user with a role higher than or equal to than you")
  guild = user.guild
  sRoles = guild.roles
  jailed = sRoles[10]
  await user.remove_roles(jailed)
  await user.add_roles(sRoles[20])
  await ctx.respond(f"{user} has been paroled")
  
client.run(token)
