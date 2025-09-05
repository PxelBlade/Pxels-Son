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
from discord import CategoryChannel
from datetime import datetime, timezone, timedelta
import pandas as pd
import csv

#Replace with your own server's ID
serverID = 928008543305629768
ownerID = 1117117776176357386
botID = 1349133273628147742

csvWriter = csv.writer(open("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", "a"))

#TEMPLATES FOR FILEPATH:
#("Folder" is there to show you how to add a folder to the path)
#Windows: C:\Folder\token.env
#Linux & Mac: ~/Folder/token.env
load_dotenv(dotenv_path="C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/token.env")

points = pd.read_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv")


token = os.getenv("TOKEN")
if token:
  print("Token found")

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="$")

owner = None

@client.event
async def on_ready():
  global owner
  owner = await client.fetch_user(int(ownerID))
  print("Bot is ready")

@client.event
async def on_guild_role_update(before, after):
   if before.permissions.administrator != after.permissions.administrator:
      await owner.send(f"A role (``{before}``)'s administrative permissions were edited") #type: ignore
   

@client.slash_command(
   name="execute",
   description="Ban a user",
   guild_ids=[serverID]
 )
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
   if user.top_role.position >= ctx.author.top_role.position:
     await ctx.respond("You cannot add a role higher than or equal to your own", ephemeral=True)
   else:
      if ctx.author == user:
            await ctx.respond(f"You can't ban yourself @taka (wait wrong person mb)", ephemeral=True)
      else:
            await user.create_dm()
            await user.send(f"You have been banned from {ctx.guild.name}. Reason: {reason}")
            await user.ban(reason=reason)
            await ctx.respond(f"{user} has been executed")
   
 
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
   await ctx.respond(f"Deleted ``{amount}`` messages")
 
@client.slash_command(
   name="revive",
   description="Unban a user",
   guild_ids=[serverID]
 )
@has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
   await ctx.guild.unban(user)
   await ctx.respond(f"Revived {user}.")
 
@client.slash_command(
   name="exile",
   description="Kick a user",
   guild_ids=[serverID]
 )
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
   if user.top_role.position >= ctx.author.top_role.position:
     await ctx.respond("You cannot kick a person with a higher than or equal role to your own", ephemeral=True)
   else:
      if ctx.author == user:
         await ctx.respond(f"You can't ban yourself @taka (wait wrong person mb)", ephemeral=True)
      else:
         await user.create_dm()
         await user.send(f"You have been kicked from {ctx.guild.name}. Reason: {reason}")
         await user.kick(reason=reason)
         await ctx.respond(f"{user} has been exiled")
 
@client.slash_command(
   name="gib",
   description="Add a role to a user",
   guild_ids=[serverID]
 )
@has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
   if role.position >= ctx.author.top_role.position:
     await ctx.respond("You cannot add a role higher than or equal to your own", ephemeral=True)
   else:
      await user.add_roles(role)
      await ctx.respond(f"Added {role} to {user}")
 
@client.slash_command(
   name="ungib",
   description="Remove a role from a user",
   guild_ids=[serverID]
 )
@has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
   if role.position >= ctx.author.top_role.position:
     await ctx.respond("You cannot remove a role higher than or equal to your own", ephemeral=True)
   else:
      await user.remove_roles(role)
      await ctx.respond(f"Removed {role} from {user}")



client.run(token)
