import os
import sys
import traceback
from time import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix="`", intents=intents, help_command=None)


@bot.event
async def on_ready():
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.moderation")
    # await bot.load_extension("cogs.automod")
    # await bot.load_extension("cogs.currency")
    # There is no automod and economy yet
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Loaded extensions")
    await bot.change_presence(activity=discord.Game(name="`help"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="Error, cannot find member",
                              description=f"I could not find member '{error.argument}'. Use `help for commands.",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error, missing arguments",
                              description=f"'{error.param.name}' is a required argument. Use `help for commands.", colour=discord.Colour.red())
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Error, command invoke error", description=f"Error: {error}\n If error says 403 missing permissions, please check bot permissions or move bot role to the top of the list.\nIf the error still persists, contact devs.",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)


    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Error, Missing permissions",
                              description=f"You are missing permissions: {error.missing_permissions}",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error, Command not found",
                              description=f"{error} is not a valid command. Use `help for commands.",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)

    else:
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@bot.command(name="help", description="List all commands")
async def commands_help(ctx):
    embed = discord.Embed(title="Commands Help", description="Commands for the bot", color=discord.Colour.green())
    embed.add_field(name="Commands",
                    value="""
                    *`help* - Shows this message
                    *`user <user>* - Shows info about a user
                    """)
    embed.add_field(name="Moderation Commands",
                    value="""
                    *Requires administrator perms*
                    *`warn <user> <reason>* - Warns a user from the server
                    *`ban <user> <delete_message_days> <reason>* - Bans a user
                    *`kick <user> <reason>* - Kicks a user
                    *`timeout <user> <duration_days> <hours> <minutes> <reason>* - Timeout user(in development - DO NOT USE)
                    *`remove_timeout <user>* - Removes a timeout from a user""")
    await ctx.send(embed=embed)


@bot.command(name="purgemsg", description="Deletes a number of messages in the channel, for testing only.")
async def purgemsg(ctx, number: int):
    sleep(1)
    msgs = []
    if 0 < number <= 100:
        async for x in ctx.history(limit=number):
            msgs.append(x)
            await ctx.channel.delete_messages(msgs)

    else:
        await ctx.send("Please enter a valid number in the range of 1-100.")
        sleep(1)
        await ctx.send("No messages were deleted.")
        return
    await ctx.send(f"{len(msgs)} messages have been deleted")




if __name__ == "__main__":
    print("Running bot...")
    sleep(5)
    if DISCORD_TOKEN is None:
        print("Error: DISCORD_TOKEN not set!")
        sys.exit(1)
    else:
        bot.run(DISCORD_TOKEN)
