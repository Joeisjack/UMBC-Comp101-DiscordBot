import discord
from discord.ext import commands
from discord import Interaction

import json
import asyncio

with open('config.json', 'r') as cfg:
    data = json.load(cfg)

TOKEN = data["token"]
bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())


# Put your discord ID here to make sure people don't hijack the bot
# The console will print out UNAUTHORIZED if you are not this ID
BOT_OPERATOR = -1

# Basically the dev-chat channel ID
# Sends some info about cleared channels here
COMMAND_CENTER = -1

# Role Names
STUDENT = "Student"
ALUMNI = "Alumni"
INCLUSIVE = "Inclusive"
INNOVATE = "Innovation"
COLLABORATE = "Collaboration"
IMPACT = "Impact"
ADAPT = "Adapt"
INSPIRE = "Inspire"
ACHIEVE = "Acheive"
UPLIFT = "Uplift"

@bot.event
async def on_ready():  # When the bot is ready
    print("Bot is online")

# Targetted Channel Wipe
# Usage: !wipe <Channel-Mention>
# Allows Op to clear a channel from a different channel
@bot.command(name = "wipe")
async def wipe(ctx, arg1):
    if ctx.author.id == BOT_OPERATOR:
        channel_id = int(arg1.strip('<#').strip('>'))

        thisChannel = bot.get_channel(channel_id).name

        channel = bot.get_channel(channel_id)

        if(channel):
            cloned_channel = await channel.clone(reason = "Wiping Channels")

            OrigChannelPos = channel.position

            # References the newly created channel and puts it in the same position as the original
            await channel.delete()

            # Important wait because sometimes is moves it too fast
            await asyncio.sleep(1)
            await cloned_channel.edit(position = OrigChannelPos)
            await ctx.send("Cleared messages in #" + thisChannel)
        else:
            await ctx.send("Channel not found. Make sure to mention the channel")
    else:
        print("UNAUTHORIZED")

# Current Channel Wipe
# Usage: !wipehere
# Allows Op to clear a channel of which the message was sent
@bot.command(name = "wipehere")
async def wipe(ctx):
    if ctx.author.id == BOT_OPERATOR:
        channel = ctx.channel

        if(channel):
            cloned_channel = await channel.clone(reason = "Wiping Channels")

            OrigChannelPos = channel.position
            await channel.delete()

            await asyncio.sleep(1)
            await cloned_channel.edit(position = OrigChannelPos)
            await bot.get_channel(int(COMMAND_CENTER)).send("Cleared messages in " + channel.name)
        else:
            await bot.get_channel(int(COMMAND_CENTER)).send("Deletion of " + ctx.channel.name + " did not work")
    else:
        print("UNAUTHORIZED")


# Wipe All Group Channels
# Usage: !wipegroups
# Wipes all channels that start with "group-"
@bot.command(name="wipegroups")
async def wipegroups(ctx):
    if ctx.author.id == BOT_OPERATOR:
        guild = ctx.guild
        channels_to_wipe = []

        # Collect all channels that start with "group-"
        for channel in guild.channels:
            if channel.name.startswith("group-"):
                channels_to_wipe.append(channel)
        
        if not channels_to_wipe:
            await ctx.send("No group channels found to wipe.")
            return
        
        await ctx.send(f"Starting to wipe {len(channels_to_wipe)} group channels...")

        for channel in channels_to_wipe:
            try:
                cloned_channel = await channel.clone(reason = "Group Wipe Command")

                OrigChannelPos = channel.position
                await channel.delete()

                await asyncio.sleep(1)
                await cloned_channel.edit(position = OrigChannelPos)
                await bot.get_channel(int(COMMAND_CENTER)).send("Cleared messages in " + channel.name)
            except Exception as e:
                await bot.get_channel(int(COMMAND_CENTER)).send(f"Failed to wipe {channel.name}: {e}")

        await ctx.send("Finished wiping group channels.")

# Verify user
# Usage: !verify <@user-mention> <Name with underscore as space> <section>
# Gives roles and sets the name of pinged user, deletes pinged user's original message, send log to dev chat
@bot.command(name = "verify")
async def verify(ctx, member: discord.Member, name, section: int):
    if ctx.author.id == BOT_OPERATOR:
        print(member, name, section)

        userGivenName = name.replace("_", " ")

        student = discord.utils.get(ctx.guild.roles, name = STUDENT)
        userSectionName = ""

        if section == 11:
            userSectionName = INCLUSIVE
        elif section == 12:
            userSectionName = INNOVATE
        elif section == 21:
            userSectionName = COLLABORATE
        elif section == 22:
            userSectionName = IMPACT
        elif section == 31:
            userSectionName = ADAPT
        elif section == 32:
            userSectionName = INSPIRE
        elif section == 41:
            userSectionName = ACHIEVE
        elif section == 42:
            userSectionName = UPLIFT

        userSection = discord.utils.get(ctx.guild.roles, name = userSectionName)

        if student and userSection is not None:
            await member.add_roles(student, userSection)
        else:
            print("Role not found")

        try:
            await member.edit(nick=userGivenName)
            print("nickname has been changed.")
        except discord.Forbidden:
            print("I don't have permission to change the nickname.")
        except discord.HTTPException as e:
            print("An error occurred")

        await bot.get_channel(int(COMMAND_CENTER)).send("user " + str(member.id) + " has been given roles Student and " + userSectionName + " with name " + userGivenName)
    else:
        print("UNAUTHORIZED")

# Update Alumni
# Usage: !updatealumni
# Gets all members with the Student role and removes all their roles. Then gives all of them the alumni role. Takes a bit to finish.
@bot.command(name = "updatealumni")
async def updatealumni(ctx):
    if ctx.author.id != BOT_OPERATOR:
        print("UNAUTHORIZED")
        return
    
    guild = ctx.guild
    studentRole = discord.utils.get(guild.roles, name=STUDENT)
    alumniRole = discord.utils.get(guild.roles, name=ALUMNI)

    if not studentRole or not alumniRole:
        await ctx.send("Required roles not found.")
        return
    
    updatedCount = 0

    for member in guild.members:
        if studentRole in member.roles:
            try:
                rolesToRemove = [role for role in member.roles if role != guild.default_role]
                await member.remove_roles(*rolesToRemove)

                await member.add_roles(alumniRole)
                print(f"Updated roles for {member.name}.")
                updatedCount += 1

            except discord.Forbidden:
                print(f"Permission error updating roles for {member.name}.")
            except discord.HTTPException as e:
                print(f"Error updating roles for {member.name}: {e}")

    await ctx.send(f"Updated {updatedCount} members from Student to Alumni.")
        

# Ping bot
# Usage: !woof
# Checks if bot is working by sending a response
@bot.command(name = "woof")
async def woof(ctx):
    if ctx.author.id == BOT_OPERATOR:
        await ctx.send("Woof!")
    else:
        print("UNAUTHORIZED")


bot.run(TOKEN)
