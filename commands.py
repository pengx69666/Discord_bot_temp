import asyncio
from datetime import datetime

import discord
from discord.ext import commands



class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, user: discord.Member):
        embed = discord.Embed(title=f"{user.name} - {user.display_name}", description="About your user:",
                              colour=discord.Colour.green())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User info:", value=f"""
        User id: {user.id}
        Username: {user.name}
        Display name: {user.display_name}""")
        embed.add_field(name="User join data",
                        value=f"Joined server: {user.joined_at.strftime("%Y-%m-%d")}\nAccount created at: {user.created_at.strftime("%Y-%m-%d")}")
        embed.add_field(name="Roles", value=", ".join([role.mention for role in user.roles]))  # Work on this
        # embed.add_field(name="Permissions", value=truncate(", ".join([f"{perm[0]}: {perm[1]}" for perm in user.guild_permissions])))
        await ctx.send(embed=embed)

    @commands.command()
    async def purge_bot(self, ctx):
        pass

    @commands.command()
    async def purge_user(self, ctx, user: discord.Member, limit: int):
        msgs = []
        async for messages in user.history(limit=limit):
            msgs.append(messages)
            await ctx.channel.delete_messages(msgs)

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(title="About this bot:", description="Created on February 22, 2024\nA testing bot for Oasis bot. We test commands(using this bot) before Oasis bot gets an update.\nThis bot is not meant for hosting 24/7.", colour=discord.Colour.blue())
        embed.add_field(name="About the developers: ", value="None")
        embed.add_field(name="Terms of service/Privacy Policy", value="None")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Commands(bot))
