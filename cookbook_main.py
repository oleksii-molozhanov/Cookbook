#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os

TOKEN = os.environ.get('COOKBOOK_BOT_TOKEN')

import logging

import telegram

#from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import command_hendlers

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("remove_recipe", command_hendlers.remove_recipe))
    application.add_handler(CommandHandler("rm", command_hendlers.remove_recipe))
    application.add_handler(CommandHandler("del", command_hendlers.remove_recipe))

    application.add_handler(CommandHandler("list", command_hendlers.list_recipes))
    application.add_handler(CommandHandler("ls", command_hendlers.list_recipes))

    application.add_handler(CommandHandler("view_recipe", command_hendlers.display_recipe))
    application.add_handler(CommandHandler("view", command_hendlers.display_recipe))
    application.add_handler(CommandHandler("vr", command_hendlers.display_recipe))

    application.add_handler(CommandHandler("new_recipe", command_hendlers.new_recipe))
    application.add_handler(CommandHandler("new", command_hendlers.new_recipe))
    application.add_handler(CommandHandler("nr", command_hendlers.new_recipe))
    application.add_handler(CommandHandler("add", command_hendlers.new_recipe))

    application.add_handler(CommandHandler("start", command_hendlers.start))
    application.add_handler(CommandHandler("help", command_hendlers.help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_hendlers.echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()