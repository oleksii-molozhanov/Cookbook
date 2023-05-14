#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

# TODO: add logger

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from cookbook import DuplicateKeyError, Cookbook
import disk_recipe_repository

recipe_repo = disk_recipe_repository.Repo()
book = Cookbook(recipe_repo)

async def remove_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if( not _command_has_arguments(update) ):
        await update.message.reply_text(f"Provide the name of a recipe you want to remove")
        return

    args = update.message.text.split()[1:]
    target_name = " ".join(args)

    try:
        recipe = book.remove_recipe(target_name)
    except KeyError:
        await update.message.reply_text(f"Could not find a recipe with the name {target_name}\n{book.list_known_recipes()}")
        return

    await update.message.reply_text(f"Removed recipe: {target_name}")


# Display details of a known recipe.
async def display_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if( not _command_has_arguments(update) ):
        await update.message.reply_text(f"Provide the name of a recipe you want to view")
        return

    args = update.message.text.split()[1:]
    target_name = " ".join(args)

    try:
        recipe = book.get_recipe(target_name)
    except KeyError:
        await update.message.reply_text(f"Could not find a recipe with the name {target_name}.\n{book.list_known_recipes()}")
        return

    await update.message.reply_text(recipe.pretty())


# List all known recipes.
async def list_recipes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(book.list_known_recipes())


# Add new recipe to the cookbook.
async def new_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if( not _command_has_arguments(update) ):
        await update.message.reply_text(f"""Creating a new recipe requires at least 1 argument - name of the new recipe.
Format of the command:
/nr name
ingredient 1
ingredient 2
etc...""")
        return

    lines = update.message.text.splitlines()
    name = " ".join( lines[0].split()[1:] )
    ingredients = lines[1:]
    #print(f"ingredients:")
    #print(ingredients)

    try:
        new_recipe = book.add_new_recipe(name, "A nice recipe", ingredients)
    except DuplicateKeyError as e:
        await update.message.reply_text(f"Recipe with the name {name} already exists")
        return
    
    await update.message.reply_text(f"New recipe created: {new_recipe.name}")


# Example.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Help.
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


# Echo.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def _command_has_arguments(update: Update) -> str:
    text_exists = update != None and update.message != None and isinstance(update.message.text, str)
    if( not text_exists ): return False

    text = update.message.text.strip()
    if( text == "" ): return False

    # First characters represent the command itself.
    args = text.split()[1:]
    if( len(args) == 0 ): return False

    return True