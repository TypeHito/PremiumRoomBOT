from pyrogram import Client, filters
from pyrogram.types import Message
from methods import user
from models import shared
from utils import const
from api import re_connection
from models import buttons


@Client.on_message(filters.private & filters.command("start"))
async def start(_: Client, msg: Message):
    try:
        await user.inset_user(shared.database, msg.from_user.id, msg.from_user.first_name, msg.from_user.is_premium)
    except Exception as err:
        return await re_connection(_, msg, err)
    else:
        current_user = await user.get_user(shared.database, msg.from_user.id)
        if current_user.phone:
            return await msg.reply_text(current_user.user_status())
        else:
            return await msg.reply_text(current_user.user_status(), reply_markup=buttons.request_contact_button(
                "📱Telefon raqamini yuborish"))


@Client.on_message(filters.contact )
async def save_start(_: Client, msg: Message):
    try:
        await user.update_contact(shared.database, msg.from_user.id, msg.contact.phone_number)
    except Exception as err:
        return await re_connection(_, msg, err)
    else:
        current_user = await user.get_user(shared.database, msg.from_user.id)
        return await msg.reply_text(current_user.user_status(), reply_markup=buttons.request_contact_button(
            "📱Telefon raqamini yuborish"))


@Client.on_message(filters.private & filters.command("my_id"))
async def my_id(_: Client, msg: Message):
    return await msg.reply_text(f"{msg.from_user.first_name} sizning ID  raqamingiz 🆔<code>{msg.from_user.id}</code>\n\n"
                                "ALGO DEMO - 7 Kunlik demo tarifi - 15 000 so'm\n"
                                "ALGO 7 - 7 Kunlik  tarifi - 500 000 so'm\n"
                                "ALGO 30 - 30 Kunlik tarifi - 1 265 000 so'm\n\n"
                                "💳VISA: <code>4176550005522077</code>\n" 
                                "💳HUMO: <code>9860176606139127</code>\n"
                                "💳HUMO: <code>9860350108599027</code>\n"
                                "❗️Eslatma: chekni @Bobur_Mirzo97 ga yuborshni unitmag.")


@Client.on_message(filters.private & filters.command("join"))
async def join(_: Client, msg: Message):
    if msg.from_user.id in const.ADMINS:
        try:
            await user.update_bot_menu(shared.database, msg.from_user.id, "join")
        except Exception as err:
            return await re_connection(_, msg, err)
        else:
            return await msg.reply_text("Telegram ID raqamini va tarifni kirinig\n"
                                        "demo - 7 kun\n"
                                        "algo7 - 7 kun\n"
                                        "algo30 - 30 kun:\n"
                                        "Misol: 1234567890 algo7")
    return await msg.reply_text("Kechirasiz, iltimosingizni tushunmadim. /start Buyruqini yuboring.")


@Client.on_message(filters.private & filters.command("ban"))
async def ban(_: Client, msg: Message):
    if msg.from_user.id in const.ADMINS:
        try:
            await user.update_bot_menu(shared.database, msg.from_user.id, "ban")
        except Exception as err:
            return await re_connection(_, msg, err)
        else:
            return await msg.reply_text("Telegram ID raqamini kiriting yoki foydalanuvchini xabarini yuboring:")
    return await msg.reply_text("Kechirasiz, iltimosingizni tushunmadim. /start Buyruqini yuboring.")
# Ban chat member forever
