from pyrogram import Client, filters
from pyrogram.types import Message
from models import shared
from models.bot_menu import BotMenu
from methods import user
from api import re_connection
from methods import message_handler
from utils import lang
from pyrogram.errors.exceptions.bad_request_400 import UserIsBot

# @Client.on_message(filters.text)
# async def message_texts(bot: Client, msg: Message):
#     print(msg.text)
#     print(msg.chat.id)


@Client.on_message(filters.private & filters.text)
async def message_text(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)

        if not current_lang:
            return await message_handler.update_language(current_user, msg)

        elif not current_user.phone:
            return await message_handler.set_phone(current_user, current_lang, msg)

        elif msg.text == BotMenu.ref:
            return await message_handler.update_ref(current_user, current_lang, msg)

        elif msg.text == current_lang["main_menu_1"]:
            return await message_handler.bot_menu_1(current_user, current_lang, msg)

        elif msg.text == current_lang["main_menu_2"]:
            return await message_handler.bot_menu_2(current_user, current_lang, msg)

        elif msg.text == current_lang["main_menu_3"]:
            return await message_handler.bot_menu_3(current_user, current_lang, msg)

        elif msg.text == current_lang["main_menu_4"]:
            return await message_handler.bot_menu_4(current_lang, msg)

        elif msg.text == current_lang["main_menu_5"]:
            return await message_handler.bot_menu_5(current_user, msg)

        elif msg.text == current_lang["main_menu_6"]:
            return await message_handler.bot_menu_6(current_lang, msg)

        elif msg.text in lang.no_lang["choice_language"]:
            return await message_handler.update_language(current_user, msg)

        elif current_user.bot_menu == BotMenu.join:
            try:
                return await message_handler.set_join(current_user, current_lang, bot, msg)
            except UserIsBot as err:
                return await msg.reply_text("message.message_text bot.join:" + str(err))

        elif current_user.bot_menu == BotMenu.ban:
            return await message_handler.set_ban(current_user, current_lang, bot, msg)

        elif current_user.bot_menu == BotMenu.ref:
            return await message_handler.update_ref(current_user, current_lang, msg)

        elif current_user.bot_menu == BotMenu.language:
            return await message_handler.update_language(current_user, msg)

    return await msg.reply_text(current_lang["warning_input"])





@Client.on_message(filters.contact)
async def save_start(bot: Client, msg: Message):
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return await re_connection(bot, msg, err)
    else:
        current_lang = user.get_current_language(current_user)

    return await message_handler.update_phone(current_user, current_lang, msg)
