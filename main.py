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
 
@client.slash_command(
   name="arrest",
   description="Arrest a user",
   guild_ids=[serverID]
 )
@has_permissions(manage_roles=True)
async def arrest(ctx, user: discord.Member, reason=None):
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
   if ctx.author.top_role.position <= user.top_role.position:
     await ctx.respond("You cannot arrest a user with a role higher than or equal to than you", ephemeral=True)
   else:
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

         
@client.slash_command(
   name="add_points",
   description="Credits a user for their contributions",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def add_points(ctx, user: discord.Member, amount: int):
   points.loc[points['ID'] == int(user.id), 'Points'] += amount
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   await ctx.respond(f"Added {amount} points to {user}.", ephemeral=True)
   await user.send(f"You have been credited {amount} points for your contributions this month. Keep up the good work!")
   if amount >= 3:
      await user.send(f"Congratulations! You reached quota for the month!")

@client.slash_command(
   name="qinfo",
   description="Check a user's current quota status",
   guild_ids=[serverID]
)
@has_role("Higher Rank")
async def points_check(ctx, user: discord.Member):
   user_points = points.loc[points['ID'] == int(user.id), 'Points']
   user_strikes = points.loc[points['ID'] == int(user.id), 'Strikes']
   if user_points.empty:
       await ctx.respond("User not found.", ephemeral=True)
       return
   user_points = user_points.values[0]
   user_strikes = user_strikes.values[0]
   await ctx.respond(f"``{user}`` has ``{user_points}`` points and ``{user_strikes}`` strikes.", ephemeral=True)
   
@client.slash_command(
   name="rem_points",
   description="Un-credits a user for their false contributions",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def rem_points(ctx, user: discord.Member, amount: int, reason=None):
   points.loc[points['ID'] == int(user.id), 'Points'] -= amount
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   await ctx.respond(f"Removed {amount} points from {user}.", ephemeral=True)
   await user.send(f"You have been deducted ``{amount}`` points for ``{reason}``.")

@client.slash_command(
   name="new_quota",
   description="Adds a member to quota",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def new_quota(ctx, user: discord.Member):
   # Append the new user to the DataFrame
   new_entry = pd.DataFrame([[user.name, user.id, 0, 0]], columns=["Name", "ID", "Points", "Strikes"])
   global points
   points = pd.concat([points, new_entry], ignore_index=True)
   
   # Save the updated DataFrame to the CSV file
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)

   await ctx.respond(f"``{user}`` has been added to the quota.", ephemeral=True)
   await user.send(f"You have been added to the quota as part as your initiation as staff. \n In order to remain in position, you must earn 3 points by the end of the month. \n To earn points, you must meet a different criteria depending on your role, which can be found below: \n \n Testers must find three bugs or show up to at least five testing sessions. \n Moderators must do at least 6 tickets (2/point). \n Developers must contribute three things to the game (more info in https://discord.com/channels/928008543305629768/1342277581222711366). Good luck!")

@client.slash_command(
   name="strike",
   description="Strikes a staff",
   guild_ids=[serverID]
)
@has_role("Pickle")
@has_role("Server Manager")
async def strike(ctx, user: discord.Member, reason: str):
   points.loc[points['ID'] == int(user.id), 'Strikes'] += 1
   user_strikes = points.loc[points['ID'] == int(user.id), 'Strikes'].values[0]
   strikesRemaining = 3 - user_strikes
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   await ctx.respond(f"``{user}`` has been striked for ``{reason}``.", ephemeral=True)
   await user.send(f"You have been striked in Find the Blades for ``{reason}``. You have {strikesRemaining} strikes left before demotion.")

@client.slash_command(
   name="forgive",
   description="Forgives a staff",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def forgive(ctx, user: discord.Member):
   points.loc[points['ID'] == int(user.id), 'Strikes'] -= 1
   user_strikes = points.loc[points['ID'] == int(user.id), 'Strikes'].values[0]
   strikesRemaining = 3 - user_strikes
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   await ctx.respond(f"``{user}`` has been forgiven. They now have {strikesRemaining} strikes remaining.", ephemeral=True)
   await user.send(f"You have been forgiven in Find the Blades. You now have {strikesRemaining} strikes remaining.")

@client.slash_command(
   name="rem_quota",
   description="Removes a member from quota",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def rem_quota(ctx, user: discord.Member):
   # Remove the user from the DataFrame
   global points
   points = points[points['ID'] != int(user.id)]
   
   # Save the updated DataFrame to the CSV file
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   
   await ctx.respond(f"``{user}`` has been removed from the quota.", ephemeral=True)
   await user.send(f"You have been removed from the quota.")

@client.slash_command(
   name="list_quota",
   description="Lists all members in quota",
   guild_ids=[serverID]
)
@has_role("Higher Rank")
async def list_quota(ctx, ephemeral: bool = True):
   global points
   points = pd.read_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv")
   quota_list = points.to_string(index=False)
   await ctx.respond(f"``{quota_list}``", ephemeral=ephemeral)

@client.slash_command(
   name="quota_reset",
   description="Resets the quota for all members",
   guild_ids=[serverID]
)
@has_role("Pickle")
async def quota_reset(ctx):
   global points
   developerRole = discord.utils.get(ctx.guild.roles, name="Developers")
   points = pd.read_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv")
   points['Points'] = 0
   points.to_csv("C:/Users/charl/OneDrive/PC backups/5-16-25 (server)/DCBot/BOT_DATA/PXELS_SON/points.csv", index=False)
   await ctx.respond("All quotas have been reset.", ephemeral=True)
   if developerRole is not None:
      await ctx.send(f"{developerRole.mention} UWA UWA ITS THE FIRST OF THE MONTH (new quota)")
   else:
      await ctx.send("UWA UWA ITS THE FIRST OF THE MONTH (new quota) (Developers role not found)")

client.run(token)
