from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import json
import calendar
from datetime import datetime, timedelta

from api import current_day, get_brons_all

with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")

def start_key():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=f"🇺🇸 eng"), KeyboardButton(text=f"🇺🇿 uz"),KeyboardButton(text=f"🇷🇺 ru"))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def ask_phone(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'contact'),request_contact=True))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def conf(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'confirm')), KeyboardButton(text=get_text(lang, 'buttons', 'rejected')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'booking')), KeyboardButton(text=get_text(lang, 'buttons', 'location')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'contactwithbarber')),KeyboardButton(text=get_text(lang, 'buttons', 'change_language')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'myorders')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


languages = ["🇺🇸 eng","🇺🇿 uz","🇷🇺 ru"]

def change_language(lang):
    keyboard = ReplyKeyboardBuilder()
    for i in languages:
        keyboard.row(KeyboardButton(text=str(i)))
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def back(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def book_barber(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'today')), KeyboardButton(text=get_text(lang, 'buttons', 'another_day')),
                         KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True)


def book_time(lang):
    keyboard = ReplyKeyboardBuilder()
    hour = current_day()
    for i in hour:
        keyboard.row(KeyboardButton(text=f'⏱️{i}'))
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)



def confirmation_time(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'confirm')), KeyboardButton(text=get_text(lang, 'buttons', 'rejected')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True)




def sana_va_hafta_kunlari(lang):
    kunlar_dict = {
        "🇺🇿 uz": ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba'],
        "🇷🇺 ru": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        "🇺🇸 eng": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }

    hafta_kunlari = kunlar_dict[lang]  # lang har doim to‘g‘ri uzatiladi deb hisoblaymiz

    ertaga = datetime.now() + timedelta(days=1)
    oy_oxiri = ertaga.replace(day=calendar.monthrange(ertaga.year, ertaga.month)[1])

    sana_dict = {}
    sana = ertaga

    while sana <= oy_oxiri:
        format_sana = sana.strftime("%d-%m")  # masalan: "14-07"
        hafta_kuni = hafta_kunlari[sana.weekday()]
        sana_dict[format_sana] = hafta_kuni
        sana += timedelta(days=1)

    return sana_dict


def test_month(lang):
    keyboard = ReplyKeyboardBuilder()
    kunlar = sana_va_hafta_kunlari(lang)

    for sana, hafta_kuni in kunlar.items():
        keyboard.row(KeyboardButton(text=f"🗒 {sana} - {hafta_kuni}"))

    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)



def check_brons_otherday(day):
    bron = get_brons_all()

    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("21:00", "%H:%M")

    all_slots = []
    current = start_time
    while current <= end_time:
        all_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    taken_slots = [v["time"] for v in bron.values() if v["date"] == day]
    slots = [t for t in all_slots if t not in taken_slots]

    return slots




def book_time_and_data(lang,day):
    keyboard = ReplyKeyboardBuilder()
    hour = check_brons_otherday(day)
    for i in hour:
        keyboard.row(KeyboardButton(text=f"⏱️ {i}"))
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def history(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'history_btn')), KeyboardButton(text=get_text(lang, 'buttons', 'cancel_booking')),
                 KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def book_time_and_dates(lang, times):
    keyboard = ReplyKeyboardBuilder()

    for time_str in times:
        # Agar vaqt jarayonda bo'lsa, ⌛ emoji qo'shamiz
        time_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        now = datetime.now()

        if time_dt >= now:  # Agar vaqt hali kelmagan bo'lsa
            emoji = "⌛"
            keyboard.row(KeyboardButton(text=f"{emoji} {time_str}"))

    # "Back" tugmasini qo'shamiz
    keyboard.add(KeyboardButton(text=get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)  # Tugmalarni 3 ta ustunda joylashtiramiz

    return keyboard.as_markup(resize_keyboard=True)