from pyrogram import Client, filters
from pyrogram.types import Message
from models import shared
from methods import user
from methods import timer
from api import re_connection
from utils import const


@Client.on_message(filters.private & filters.text)
async def private_message(_: Client, msg: Message):
    try:
        current_client = await user.get_user(shared.database, msg.from_user.id)
    except Exception as err:
        return re_connection(err)
    else:
        if current_client.bot_menu == "join":
            try:
                telegram_id, tariff = msg.text.split(" ")
            except ValueError:
                return await msg.reply_text(f"Xatolik . . . (00000000 tariff) formatda kiriting")
            if tariff in ["algo7", "demo"]:
                await user.update_subscription(shared.database, int(telegram_id), current_client.telegram_id,
                                               timer.get_current_time(), timer.get_end_time(7))
            elif tariff == "algo30":
                await user.update_subscription(shared.database, int(telegram_id), current_client.telegram_id,
                                               timer.get_current_time(), timer.get_end_time(30))
            else:
                return await msg.reply_text(f"Xatolik . . .")
            await user.update_bot_menu(shared.database, msg.from_user.id, "")
            link = await _.create_chat_invite_link(const.CHANNEL, member_limit=1)
            await _.send_message(int(telegram_id), f"ESLATMA!!!!!\nushbu havola bir martalik \n{link.invite_link}")

            return await msg.reply_text(f"{telegram_id} ga {tariff}  muvofaqqiyatli aktivlashtirildi.")
        elif current_client.bot_menu == "ban":
            await user.update_subscription_end(shared.database, int(msg.text), msg.from_user.id, timer.get_current_time())
            await _.ban_chat_member(const.CHANNEL, int(msg.text))
            await user.update_bot_menu(shared.database, msg.from_user.id, "")
            return await msg.reply_text(f"{msg.text} muvofaqqiyatli diaktivlashtirildi.")
        return await msg.reply_text("Kechirasiz, iltimosingizni tushunmadim. /start Buyruqini yuboring.")


@Client.on_message(filters.text)
async def private_message(_: Client, msg: Message):
    return print(msg.chat.id)