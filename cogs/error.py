"""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (c) 2021 gunyu1019

YBOT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YBOT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YBOT.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging

import discord
from discord.ext import commands
from discord.ext import interaction

logger = logging.getLogger(__name__)


class Error:
    def __init__(self, bot: interaction.Client):
        self.bot = bot

        # CommandTree - CommandNotFound for issue fix
        # will be delete at discord-extension-interaction v0.6~
        bot.tree.on_error = self.dummy_on_error

    @staticmethod
    async def dummy_on_error(*_1, **_2):
        pass

    def _traceback_msg(self, tb):
        if tb.tb_next is None:
            return f"{tb.tb_frame.f_code.co_filename} {tb.tb_frame.f_code.co_name} {tb.tb_lineno}줄 "
        return f"{tb.tb_frame.f_code.co_filename} ({tb.tb_frame.f_code.co_name}) {tb.tb_lineno}줄\n{self._traceback_msg(tb.tb_next)}"

    @commands.Cog.listener()
    async def on_interaction_command_error(self, ctx, error):
        if error.__class__ == discord.ext.commands.errors.CommandNotFound:
            return
        elif error.__class__ == discord.ext.commands.CheckFailure:
            embed = discord.Embed(
                title="\U000026A0 에러", description="권한이 부족합니다.", color=0xAA0000
            )
            await ctx.send(embed=embed)
            return
        exc_name = type(error)
        exc_list = [str(x) for x in error.args]

        if not exc_list:
            exc_log = exc_name.__name__
        else:
            exc_log = "{exc_name}: {exc_list}".format(
                exc_name=exc_name.__name__, exc_list=", ".join(exc_list)
            )

        error_location = self._traceback_msg(error.__traceback__)

        if ctx.guild is not None:
            logger.error(
                f"({ctx.guild.name}, {ctx.channel.name}, {ctx.author}, {ctx.content}): {exc_log}\n{error_location}"
            )
        else:
            logger.error(
                f"({ctx.channel},{ctx.author},{ctx.content}): {exc_log}\n{error_location}"
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ctx.content = ""
        if ctx.message is not None:
            ctx.content = ctx.message.content
        await self.on_interaction_command_error(ctx, error)


async def setup(client):
    client.add_icog(Error(client))
