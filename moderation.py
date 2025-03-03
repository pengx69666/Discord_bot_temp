from datetime import timedelta

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = "None"):
        if user.id == user.bot:
            await ctx.send("Cannot warn bots")
            return

        embed = discord.Embed(title="You have been warned", description=f"Server: {ctx.message.guild.name}",
                              colour=discord.Colour.green())
        embed.add_field(name="Reason:", value={reason})
        await user.send(embed=embed)
        # save warn into database with user id

        # await warning.send(embed=embed)
        await ctx.send(f"Warned {user.mention}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_warnings(self, ctx, user: discord.Member):
        # Get user id warnings from database
        # then list warnings
        ...

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member, delete_message_days: int = 0, *, reason: str = "None"):
        if user.id == user.bot:
            await ctx.send("You cannot ban bots. If you want to remove a bot, use `kick.")
            return
        embed = discord.Embed(title="You have been banned", description=f"Server: {ctx.message.guild.name}",
                              colour=discord.Colour.green())
        embed.add_field(name="Reason:", value=reason)
        await user.send(embed=embed)
        await user.ban(delete_message_days=delete_message_days, reason=reason)
        await ctx.send(f"Banned {user.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = "None"):
        embed = discord.Embed(title="You have been kicked", description=f"Server: {ctx.message.guild.name}",
                              colour=discord.Colour.green())
        embed.add_field(name="Reason: ", value=reason)
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def timeout(self, ctx, user: discord.Member, duration_days: int, duration_hours: int, duration_minutes: int,
                      *, reason: str = "None"):
        embed = discord.Embed(
            title=f"{user.mention} got a timeout for {duration_days} days, {duration_hours} hours, and {duration_minutes} minutes",
            description=f"Reason: {reason}")
        if duration_days <= 28 and duration_hours <= 672 and duration_minutes <= 40320:
            if duration_days * 1440 + duration_hours * 60 + duration_minutes <= 40320:
                minutes = duration_days * 1440 + duration_hours * 60 + duration_minutes
                timeout_duration = timedelta(minutes=minutes)
                await user.timeout(timeout_duration, reason=reason)
                await ctx.send(embed=embed)
            else:
                await ctx.send("The duration has to be less or equal to 28 days.")
        else:
            await ctx.send("Use a valid duration.")
        # Working on this

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_timeout(self, ctx, user: discord.Member):
        embed = discord.Embed(title=f"Removed timeout for {user.mention}")
        await user.timeout(None)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_nick(self, ctx, user: discord.Member, *, nick: str):
        await user.edit(nick=nick)
        await ctx.send(f"{user.mention}'s server nickname has been changed to {nick}")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
