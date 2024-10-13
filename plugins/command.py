from methods import command_handler
from methods import invoice_handler
from models.bot_menu import BotMenu
from pyrogram import Client, filters
from pyrogram.types import Message
from methods import user
from models import shared
from api import re_connection


@Client.on_message(filters.private & filters.command(BotMenu.start))
async def start(_: Client, msg: Message):
    await command_handler.command_start(msg)


@Client.on_message(filters.private & filters.command(BotMenu.my_id))
async def my_id(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)
        await command_handler.my_id(current_user, current_lang, msg)


@Client.on_message(filters.private & filters.command(BotMenu.join))
async def join(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)
        await command_handler.join(current_user, current_lang, bot, msg)


@Client.on_message(filters.private & filters.command(BotMenu.ban))
async def ban(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)
        await command_handler.ban(current_user, current_lang, bot, msg)


@Client.on_message(filters.private & filters.command(BotMenu.algo30))
async def send_invoice(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)
        await invoice_handler.init_invoice(bot, msg)
