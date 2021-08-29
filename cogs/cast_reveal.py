#!/usr/bin/env python3.8
import asyncio
import importlib
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from random import shuffle
from typing import List

import discord
from discord.ext import commands

import common.cards as cards


class CastReveal(commands.Cog, name="Cast Reveal"):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.is_owner()
    async def cast_reveal(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send(
            "Preparing cast reveal. One person will be revealed roughly every minute. "
            + "All entries were randomly shuffled beforehand.\n```\n \n```"
        )

        applied = discord.Object(786619063023566899)
        alive_player = discord.Object(786610731826544670)

        shuffled_participants = deepcopy(cards.participants)
        shuffle(shuffled_participants)

        async with ctx.typing():
            await asyncio.sleep(10)  # because otherwise it would be done a bit too fast

            for card in shuffled_participants:
                after_cooldown = discord.utils.utcnow() + timedelta(seconds=60)

                embed = await card.as_embed(ctx.bot)
                await ctx.send(
                    f"**Welcome {card.title_name}!**\nBy: {card.mention}", embed=embed
                )
                await ctx.send("```\n \n```")  # looks neater

                member = ctx.guild.get_member(card.user_id)
                await member.remove_roles(applied)
                await member.add_roles(alive_player)

                await discord.utils.sleep_until(after_cooldown)

        await ctx.send(
            "**All participants have been revealed.**\nWe apologize if you didn't get in, "
            + "but there were quite a number of applications this season (39, in fact). "
            + "Astrea will be sending a concluding message shortly about backups and other details."
        )


def setup(bot):
    importlib.reload(cards)
    bot.add_cog(CastReveal(bot))
