from aiogram.types import KeyboardButton, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import json

with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")

def start_key():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=f"🇺🇸 eng"), KeyboardButton(text=f"🇺🇿 uz"),
                 KeyboardButton(text=f"🇷🇺 ru"))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def phone_key(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'contact'),request_contact=True))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def back(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)

def conf(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'confirm')), KeyboardButton(text=get_text(lang, 'buttons', 'rejected')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'menu_btn1')), KeyboardButton(text=get_text(lang, 'buttons', 'menu_btn2')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'menu_btn3')),KeyboardButton(text=get_text(lang, 'buttons', 'menu_btn4')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'language')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def menu_admin(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'admin_menu1')), KeyboardButton(text=get_text(lang, 'buttons', 'admin_menu2')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'admin_menu3')),KeyboardButton(text=get_text(lang, 'buttons', 'admin_menu4')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)