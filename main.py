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

#Replace with your own server's ID
serverID = 928008543305629768
ownerID = 1117117776176357386
botID = 1349133273628147742

#TEMPLATES FOR FILEPATH:
#("Folder" is there to show you how to add a folder to the path)
#Windows: C:\Folder\token.env
#Linux & Mac: ~/Folder/token.env
load_dotenv(dotenv_path="C:/Users/charl/AuthKeys/key.env")

token = os.getenv("TOKEN")
if token:
  print("Token found")

intents = discord.Intents.all()
client = commands.Bot(intents=intents)

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
 
@client.slash_command(
   name="arrest",
   description="Arrest a user",
   guild_ids=[serverID]
 )
@has_permissions(manage_roles=True)
async def arrest(ctx, user: discord.Member, reason=None):
   if ctx.author.top_role.position <= user.top_role.position:
     await ctx.respond("You cannot arrest a user with a role higher than or equal to than you", ephemeral=True)
   guild = user.guild
   sRoles = guild.roles
   jailed = None
   for i in sRoles:
     if i.name == "Jailed":
       jailed = i
       break
   if jailed is None:
       await ctx.respond("The 'Jailed' role does not exist.", ephemeral=True)
       return
   await user.edit(roles=[])
   await user.add_roles(jailed)
   await user.move_to(None) #Kicks from VC (This is the only thing I find confusing to code)
   await ctx.respond(f"{user} has been arrested")
   await user.create_dm()
   await user.send(f"You have been arrested in {ctx.guild.name} for {reason}")
 
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

@client.slash_command(
    name="ticket",
    description="Create a ticket",
    guild_ids=[serverID]
)
@has_role("Novice [10]")
async def ticket(ctx):
    if has_role == False:
       ctx.respond("Invalid permissions! Level 10 is required to create a ticket.", ephemeral=True)
    guild = ctx.guild
    ticketer = None 
    for i in guild.roles:
        if i.name == "Ticketers":
            ticketer = i
            break
    if ticketer is None:
        await ctx.respond("The 'Ticketer' role does not exist.")
        return
    category = get(guild.categories, name="Tickets")
    if category is None:
        await ctx.respond("The 'Tickets' category does not exist.")
        return
    channel = await category.create_text_channel(name=f"ticket-{ctx.author}")
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await channel.set_permissions(ticketer, read_messages=True, send_messages=True)
    await ctx.respond(f"Ticket created: {channel.mention}", ephemeral=True)
    await channel.send(f"{ctx.author.mention} please describe your issue. A moderator will arise from the dead soon to assist you.")
    ticketChannel = guild.get_channel(1350681276918661128)
    currentTime = datetime.now(timezone.utc)
    timestamp_str = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    await ticketChannel.send(f"{ticketer.mention} ``{ctx.author}`` has opened a ticket at ``{timestamp_str}`` UTC.")

@client.slash_command(
   name="point_request",
   description="Sends a request to get quota points",
   guild_ids=[serverID]
)
@has_role("Higher Rank")
async def point_request(ctx, amount: int, reason: str):
   await owner.send(f"``{ctx.author}`` has requested the addition of ``{amount}`` points for ``{reason}``.") #type: ignore
   await ctx.respond(f"Your point request has been submitted successfully!", ephemeral=True)
   
@client.slash_command(
   name="close",
   description="Closes the current ticket",
   guild_ids=[serverID]
)
@has_role("Ticketers")
async def close(ctx, reason="no reason"):
   guild = ctx.guild
   cats = guild.categories
   ticketChannel = guild.get_channel(1350681276918661128)
   currentTime = datetime.now(timezone.utc)
   timestamp_str = currentTime.strftime("%Y-%m-%d %H:%M:%S")
      
   if ctx.channel.category.id == 1350926649293672589:
      await ctx.channel.delete()
      await ticketChannel.send(f"Ticket closed at ``{timestamp_str}`` UTC by ``{ctx.author}`` for ``{reason}``.")
   else:
      await ctx.respond(f"This channel isn't a ticket!", ephemeral=True)

@client.slash_command(
   name="clear",
   description="clears all bot messages",
   guild_ids=[serverID]
)
@has_role("Higher Rank")
async def clear(ctx):
   async for i in ctx.channel.history(limit=None):
      if i.author.id == botID:
         await i.delete()
      else:
         break
   await ctx.respond("All bot messages deleted!", ephemeral=True)

         
      







client.run(token)
