# Yes, I am aware that this is open source
# This is supposed to be an exclusive bot
# You can fork and customize, but DO NOT USE THIS TO IMPERSONATE ME

import json
import os
from dotenv import load_dotenv

import time

import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands.core import has_permissions, has_role

load_dotenv(dotenv_path="token.env")

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
guild_ids=[928008543305629768]
)
async def ping(ctx):
  await ctx.respond(f"Pong! {round(client.latency * 1000)}ms")

@client.slash_command(
  name="ban",
  description="Ban a user",
  guild_ids=[928008543305629768]
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
  guild_ids=[928008543305629768]
)
@has_role("Developers")
async def dm(ctx, user: discord.Member, *, message):
  await user.send(message)
  await ctx.respond(f"Sent message to {user}")

@client.slash_command(
  name="purge",
  description="Delete messages",
  guild_ids=[928008543305629768]
)
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount)
  await ctx.respond(f"Deleted {amount} messages")
  time.sleep(3)
  await ctx.channel.purge(limit=1)

@client.slash_command(
  name="unban",
  description="Unban a user",
  guild_ids=[928008543305629768]
)
@has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
  await ctx.guild.unban(user)
  await ctx.respond(f"Unbanned {user}")

@client.slash_command(
  name="kick",
  description="Kick a user",
  guild_ids=[928008543305629768]
)
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.create_dm()
  await user.send(f"You have been kicked from {ctx.guild.name}. Reason: {reason}")
  await user.kick(reason=reason)
  await ctx.respond(f"{user} has been kicked")

@client.slash_command(
  name="addrole",
  description="Add a role to a user",
  guild_ids=[928008543305629768]
)
@has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
  await user.add_roles(role)
  await ctx.respond(f"Added {role} to {user}")
  if user.top_role.position > ctx.author.top_role.position:
    await ctx.respond("You cannot add a role higher than your own")

@client.slash_command(
  name="removerole",
  description="Remove a role from a user",
  guild_ids=[928008543305629768]
)
@has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
  await user.remove_roles(role)
  await ctx.respond(f"Removed {role} from {user}")
  if user.top_role.position > ctx.author.top_role.position:
    await ctx.respond("You cannot remove a role higher than your own")
  
  


client.run(token)
