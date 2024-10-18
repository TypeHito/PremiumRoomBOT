from api import re_connection
from methods import user
from models import buttons
from models import shared
from models.bot_menu import BotMenu
from utils import lang
from utils import const


async def command_start(msg):
    command, value = msg.command if len(msg.command) > 1 else (msg.command[0], None)
    await msg.reply_text(lang.no_lang["send_start_info"])
    await msg.reply_text(lang.no_lang["send_start_channel"])
    if value:
        referral_id = user.get_referral_id(value)
        try:
            referral = await user.get_user(shared.database, referral_id)
        except ValueError:
            referral = None
        await user.update_referral_count(shared.database, referral)
        await user.inset_user(shared.database, msg, referral_id)

    else:
        await user.inset_user(shared.database, msg)
    try:
        current_user = await user.get_user(shared.database, msg.from_user.id)
    except AttributeError:
        return
    current_lang = user.get_current_language(current_user)

    if current_lang == {}:
        await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.language)
        return await msg.reply_text(lang.no_lang["choice_language"], reply_markup=buttons.languages())
    elif not current_user.phone:
        return await msg.reply_text(current_user.user_status(current_lang),
                                    reply_markup=buttons.request_contact_button(current_lang["send_contact"]))
    else:

        await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.delete)

        return await msg.reply_text(current_user.user_status(current_lang), reply_markup=buttons.main_manu(current_lang))


async def my_id(current_user, current_lang, msg):

    return await msg.reply_text(current_lang["my_id"].format(current_user.first_name, current_user.telegram_id))


async def join(current_user, current_lang, bot, msg):
    if current_user.telegram_id in const.ADMINS:
        try:
            await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.join)
        except Exception as err:
            return await re_connection(bot, msg, err)
        else:
            return await msg.reply_text(current_lang["join"])

    return await msg.reply_text(current_lang["warning_input"])


async def ban(current_user, current_lang, bot, msg):
    if current_user.telegram_id in const.ADMINS:
        try:
            await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.ban)
        except Exception as err:
            return await re_connection(bot, msg, err)
        else:
            return await msg.reply_text(current_lang["ban"])
    return await msg.reply_text(current_lang["warning_input"])
