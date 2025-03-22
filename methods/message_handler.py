from methods import timer
from models import buttons
from models import shared
from methods import user
from models.bot_menu import BotMenu
from utils import const
from utils import lang
from pyrogram.errors.exceptions.bad_request_400 import UserAdminInvalid, BadRequest, PeerIdInvalid


async def set_ref(current_user, current_lang, msg):
    if current_user.referral_id:
        await msg.reply_text(current_lang["warning_have_ref"])
    else:
        await user.update_bot_menu(shared.database, msg.from_user.id, BotMenu.ref)
        return await msg.reply_text(current_lang["send_ref"])


async def update_ref(current_user, current_lang, msg):
    await user.update_bot_menu(shared.database, msg.from_user.id, BotMenu.ref)
    try:
        referral_id = int(msg.text)
    except ValueError:
        return await msg.reply_text(current_lang["warning_ref_number"])
    try:
        referral = await user.get_user(shared.database, referral_id)
    except TypeError:
        return await msg.reply_text(current_lang["warning_ref"])
    if referral_id != current_user.telegram_id:
        await user.update_referral(shared.database, current_user.telegram_id, int(msg.text))
        await user.update_referral_count(shared.database, referral)
        return await msg.reply_text(current_lang["set_ref"].format(referral_id))
    else:
        return await msg.reply_text(current_lang["warning_ref_self"])


async def set_phone(current_user, current_lang, msg):
    await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.delete)
    return await msg.reply_text(
        current_lang["send_contact"],
        reply_markup=buttons.request_contact_button(
            current_lang["send_contact"]
        )
    )


async def update_phone(current_user, current_lang, msg):
    await user.update_contact(shared.database, current_user.telegram_id, msg.contact.phone_number)
    return await msg.reply_text(current_user.user_status(current_lang), reply_markup=buttons.main_manu(current_lang))


async def set_language(current_user, msg):
    # Here sent languages
    await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.language)
    return await msg.reply_text(lang.no_lang["choice_language"], reply_markup=buttons.languages())


async def update_language(current_user, msg):
    if msg.text in const.LANGUAGES:
        new_lang = lang.langs[const.LANGUAGES[msg.text]]
        await user.update_language(shared.database, current_user.telegram_id, const.LANGUAGES[msg.text])
        if current_user.phone:
            return await msg.reply_text(msg.text + new_lang["set_language"],
                                        reply_markup=buttons.main_manu(new_lang))
        else:
            await msg.reply_text(new_lang["set_language"], reply_markup=buttons.main_manu(lang.langs[const.LANGUAGES[msg.text]]))
            await set_phone(current_user, new_lang, msg)
    else:
        return await msg.reply_text(lang.no_lang["warning_lang"], reply_markup=buttons.languages())


async def set_join(current_user, current_lang, bot, msg):
    try:
        telegram_id, tariff = msg.text.split(" ")
    except ValueError:
        return await msg.reply_text(current_lang["warning_join"])
    if tariff == "algogold":
        await user.update_subscription(shared.database, int(telegram_id), current_user.telegram_id,
                                       timer.get_current_time(), timer.get_end_time(30))
        try:
            await bot.unban_chat_member(const.CHANNELS[1], int(telegram_id))
            await bot.unban_chat_member(const.CHAT_ID, int(telegram_id))
        except BadRequest as err:
            await msg.reply_text(str(err))
            return await bot.send_message(const.ADMINS[0], "message_handler.set_join: " + str(err))
        channel_link = await bot.create_chat_invite_link(const.CHANNELS[1], member_limit=1)
        await bot.send_message(int(telegram_id), current_lang['warning_link'].format(channel_link.invite_link))
        await bot.send_message(int(telegram_id), current_lang['warning_link'].format(const.CHAT))
        await bot.send_message(int(telegram_id), "https://telegra.ph/Signallar-haqida-tushuncha-03-12")


    elif tariff == "algo30":
        await user.update_subscription(shared.database, int(telegram_id), current_user.telegram_id,
                                       timer.get_current_time(), timer.get_end_time(30))
        try:
            await bot.unban_chat_member(const.CHANNELS[0], int(telegram_id))
            await bot.unban_chat_member(const.CHAT_ID, int(telegram_id))
        except BadRequest as err:
            await msg.reply_text(str(err)+"bad request from algo30")
            return await bot.send_message(const.ADMINS[0], "message_handler.set_join: " + str(err))
        channel_link = await bot.create_chat_invite_link(const.CHANNELS[0], member_limit=1)
        await bot.send_message(int(telegram_id), current_lang['warning_link'].format(channel_link.invite_link))
        await bot.send_message(int(telegram_id), current_lang['warning_link'].format(const.CHAT))
        await bot.send_message(int(telegram_id), "https://telegra.ph/Signallar-haqida-tushuncha-03-12")
    else:
        return await msg.reply_text(current_lang["warning_join_tariff"])
    await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.delete)
    return await msg.reply_text(f"{telegram_id} ga {tariff}  muvofaqqiyatli aktivlashtirildi.")


async def set_ban(current_user, current_lang, bot, msg):
    await user.update_subscription_end(shared.database, int(msg.text), current_user.telegram_id)
    try:
        for channel in range(len(const.CHANNELS)):
            try:
                await bot.ban_chat_member(const.CHANNELS[channel], int(msg.text))
            except ValueError as err:
                await bot.send_message(const.ADMINS[0], str(err))

        await bot.send_message(int(msg.text),  lang.no_lang["end_time"])
        try:
            await bot.ban_chat_member(const.CHAT_ID, int(msg.text))
        except PeerIdInvalid as err:
            return msg.reply_text(str(err))
    except UserAdminInvalid as err:
        await msg.reply_text(str(err))
        return await bot.send_message(const.ADMINS[0], "message_handler.set_ban: " + str(err))
    else:
        await user.update_bot_menu(shared.database, current_user.telegram_id, BotMenu.delete)

    return await msg.reply_text(current_lang["set_ban"].format(msg.text))


async def bot_menu_1(current_user, current_lang, msg):
    return await msg.reply_text(current_user.user_status(current_lang), reply_markup=buttons.main_manu(current_lang))


async def bot_menu_2(current_user, current_lang, msg):
    return await msg.reply_text(current_lang["my_id"].format(current_user.first_name, current_user.telegram_id))


async def bot_menu_3(current_user, current_lang, msg):
    return await set_ref(current_user, current_lang, msg)


async def bot_menu_4(current_lang, msg):
    return await msg.reply_text(current_lang["about_us"])


async def bot_menu_5(current_user, msg):
    return await set_language(current_user, msg)


async def bot_menu_6(current_lang, msg):
    return await msg.reply_text(str(current_lang["my_id_is"]).format(msg.from_user.id))
