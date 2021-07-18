import time

from discord.ext import commands


class EtcCmds(commands.Cog, name="Misc."):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot. Great way of finding out if the bot’s working correctly, but otherwise has no real use."""

        start_time = time.perf_counter()
        ping_discord = round((self.bot.latency * 1000), 2)

        mes = await ctx.reply(
            f"Pong!\n`{ping_discord}` ms from Discord.\nCalculating personal ping..."
        )

        end_time = time.perf_counter()
        ping_personal = round(((end_time - start_time) * 1000), 2)

        await mes.edit(
            content=f"Pong!\n`{ping_discord}` ms from Discord.\n`{ping_personal}` ms personally."
        )


def setup(bot):
    bot.add_cog(EtcCmds(bot))