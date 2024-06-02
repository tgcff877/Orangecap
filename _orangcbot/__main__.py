from __future__ import annotations

from os import environ, getenv
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
import os
import traceback

import nextcord
import psycopg2
from nextcord import ApplicationError, Intents
from nextcord.ext import application_checks as ac
from nextcord.ext import commands, help_commands

prefix = "oct/" if os.getenv("TEST") else "oc/"


class ConvertibleToInt:
    def __int__(self) -> int: ...


class OrangcBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        # self._db: psycopg2.connection = psycopg2.connect(
        #     host=getenv("DBHOST"),
        #     user=getenv("DBUSER"),
        #     port=getenv("DBPORT"),
        #     password=getenv("DBPASSWORD"),
        #     dbname=getenv("DBNAME"),
        # )
        super().__init__(*args, **kwargs)

    async def on_command_error(
        self, context: commands.Context, error: Exception
    ) -> None:
        if isinstance(error, commands.NotOwner):
            await context.send("Impersonator")
        elif isinstance(error, commands.UserInputError):
            await context.send("Such a fool can't read help")
        elif isinstance(error, commands.CommandNotFound):
            await context.send("Imagine disillusioned")
        elif isinstance(error, commands.errors.DisabledCommand):
            await context.send("Shhhhhhhh")
        else:
            await context.send("Fool")
            await super().on_command_error(context, error)

    async def on_application_command_error(
        self, interaction: nextcord.Interaction, exception: ApplicationError
    ) -> None:
        if isinstance(exception, ac.ApplicationMissingRole):
            await interaction.send("Imagine not being a staff")
        else:
            await interaction.send("Fool")
            await super().on_application_command_error(interaction, exception)


def convert_none_to_0(key: Optional[ConvertibleToInt] = None) -> int:
    if key == None:
        return 0
    else:
        return int(key)


owner_ids = [716134528409665586]
if not convert_none_to_0(os.getenv("TEST")):  # type: ignore[reportArgumentType]
    owner_ids.append(853158265466257448)

bot = OrangcBot(
    intents=Intents.all(),
    command_prefix=prefix,
    help_command=help_commands.PaginatedHelpCommand(),
    case_insensitive=True,
    owner_ids=owner_ids,
    allowed_mentions=nextcord.AllowedMentions.none(),
)
# @bot.event
# async def on_command_error(ctx, error):
#     k = await ctx.bot.create_dm(nextcord.Object(id=716134528409665586))
#     await k.send(traceback.format_exception(error))
#     print(traceback.format_exception(error))

bot.load_extension("onami")
bot.load_extension("extensions.fun")
bot.load_extension("extensions.faq")
bot.load_extension("extensions.antiphishing")
bot.load_extension("extensions.testing_functions")
bot.load_extension("extensions.nonsense")
bot.load_extension("extensions.dns")
bot.load_extension("extensions.suggestions")
bot.load_extension("extensions.delete_response")
bot.load_extension("extensions.nixwiki")
bot.load_extension("extensions.archwiki")
bot.load_extension("extensions.github")
bot.load_extension("extensions.swiftie")
if os.getenv("HASDB"):
    bot.load_extension("extensions.tags_reworked")
# bot.load_extension("extensions.forum")
bot.run(environ["TOKEN"])
