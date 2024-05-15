from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                            InlineKeyboardButton)


def request_contact_button(text):
    kb = [[KeyboardButton(text, request_contact=True)]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)


def ok_cancel(ok, cancel):
    kb = [InlineKeyboardButton("ok", ok), InlineKeyboardButton("cancel", cancel)]
    return InlineKeyboardMarkup([kb])


def get_start(get, start):
    kb = [InlineKeyboardButton(get, "get"), InlineKeyboardButton(start, "start")]
    return InlineKeyboardMarkup([kb])


def main_manu(strings, is_admin=False):
    kb = [
        [KeyboardButton(strings["main_menu_1"]), KeyboardButton(strings["main_menu_2"])],
        [KeyboardButton(strings["main_menu_3"])]
    ]
    # kb['keyboard'].append([reply_keyboard_button(strings["send_number"], request_contact=True)])
    if is_admin:
        kb.append([KeyboardButton("GetList")])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)