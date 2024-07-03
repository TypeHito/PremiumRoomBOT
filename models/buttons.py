from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from utils import const


def request_contact_button(text):
    kb = [[KeyboardButton(text, request_contact=True)]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)


def ok_cancel(ok, cancel):
    kb = [InlineKeyboardButton("ok", ok), InlineKeyboardButton("cancel", cancel)]
    return InlineKeyboardMarkup([kb])


def get_start(get, start):
    kb = [InlineKeyboardButton(get, "get"), InlineKeyboardButton(start, "start")]
    return InlineKeyboardMarkup([kb])


def languages():
    kb = [[KeyboardButton(lang)] for lang in const.LANGUAGES]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)


def main_manu(strings, is_admin=False):
    kb = [
        [KeyboardButton(strings["main_menu_1"])],
        [KeyboardButton(strings["main_menu_2"]), KeyboardButton(strings["main_menu_3"])],
        [KeyboardButton(strings["main_menu_4"])],
        [KeyboardButton(strings["main_menu_5"])]
    ]
    if is_admin:
        kb.append([KeyboardButton("GetList")])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False)