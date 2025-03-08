# Yes, I am aware that this is open source
# This is supposed to be an exclusive bot
# You can fork and customize, but DO NOT USE THIS TO IMPERSONATE ME

import json
import os

import time

import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands.core import has_permissions, has_role

token = "MTExODYyOTk0NDk2NTIwNjA4Nw.GKUIsp.DWE9IhCV0EjBOXEyGRiiIM5pvQl6gP0p2M03F8"

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
  
  


client.run(token)
