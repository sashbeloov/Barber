import json
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime, timedelta
from decouple import config

from api import create_user, update_user_lang, get_user_by_telegram_id, current_day, booked_time, booking_history_user
#local
from state import statuslar
import keyboard as kb

TOKEN = config('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


admin_id = [8004593517]

with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)


def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")



user_lang = {"uz":"🇺🇿 uz", "eng":"🇺🇸 eng", "ru":"🇷🇺 ru"}
@router.message(F.text.startswith("/start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in get_user_by_telegram_id():
        lang = user_lang[get_user_by_telegram_id()[user_id]]
        await state.update_data(language=lang)
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb.menu(lang))
        await state.set_state(statuslar.menu)
    else:
        await bot.send_message(
            chat_id=user_id,
            text=translations['start'],
            reply_markup=kb.start_key(),
            parse_mode='HTML'
        )
        await state.set_state(statuslar.language)




@router.message(statuslar.language)
async def ask_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text in {"🇺🇸 eng":"🇺🇸 eng","🇺🇿 uz":"🇺🇿 uz","🇷🇺 ru":"🇷🇺 ru",}:
        await state.update_data(language=message.text)
        data = await state.get_data()
        lang = data['language']
        await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'contact'), reply_markup=kb.ask_phone(lang))
        await state.set_state(statuslar.phone)



@router.message(statuslar.phone)
async def check_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'user_info'), reply_markup=ReplyKeyboardRemove())
        await state.set_state(statuslar.fio)
    else:
        text = message.text
        if message.text.startswith("+998") and len(text) == 13 and text[1:].isdigit():
            await state.update_data(phone=message.text)
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'user_info'), reply_markup=ReplyKeyboardRemove())
            await state.set_state(statuslar.fio)
        else:
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'error_phone'))


@router.message(statuslar.fio)
async def fio_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    ok = True
    for i in message.text:
        if not i.isalpha():
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'error_name'))
            ok = False
            break
    if ok:
        await state.update_data(user_name=message.text)
        msg_text = (
            f"{get_text(lang, 'message_text', 'show_info')}\n"
            f"{get_text(lang, 'message_text', 'phone')} {data["phone"]}\n"
            f"{get_text(lang, 'message_text', 'name')} {message.text}"
        )

        await bot.send_message(chat_id=user_id,text=msg_text, reply_markup=kb.conf(lang))
        await state.set_state(statuslar.conf)




@router.message(statuslar.conf)
async def conf(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "confirm"):
        if create_user(data["phone"],data["user_name"],str(user_id),lang):
            await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb.menu(lang))
            await state.set_state(statuslar.menu)

    elif message.text == get_text(lang, "buttons", "rejected"):
        await bot.send_message(chat_id=user_id, text=translations['start'], reply_markup=kb.start_key(), parse_mode='HTML')
        await state.set_state(statuslar.language)




@router.message(statuslar.menu)
async def menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "change_language"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'change_language'),reply_markup=kb.change_language(lang))
        await state.set_state(statuslar.change_language)
    elif message.text == get_text(lang, "buttons", "location"):
        await bot.send_location(chat_id=user_id, latitude=41.331411, longitude=69.252588)
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'location'),reply_markup=kb.back(lang))
        await state.set_state(statuslar.location)
    elif message.text == get_text(lang, "buttons", "contactwithbarber"):
        await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'barber_info'), reply_markup=kb.back(lang))
        await state.set_state(statuslar.barber_contact)
    elif message.text == get_text(lang, "buttons", "booking"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'book_barber'),reply_markup=kb.book_barber(lang))
        await state.set_state(statuslar.book_barber)
    elif message.text == get_text(lang, "buttons", "myorders"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'history'),reply_markup=kb.history(lang))
        await state.set_state(statuslar.orderhistory)


@router.message(statuslar.orderhistory)
async def cancel_and_history(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']

    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'),
                               reply_markup=kb.menu(lang))
        await state.set_state(statuslar.menu)

    elif message.text == get_text(lang, "buttons", "history_btn"):
        times = booking_history_user(user_id)
        if times:
            all_time = ""
            now = datetime.now()

            for time_str in times:
                time_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

                # Vaqt hali kelmagan (yoki hozirgi vaqtdan keyin)
                if time_dt >= now:
                    emoji = "⌛"  # Jarayonda
                else:
                    emoji = "✅"  # O‘tgan

                all_time += f"{emoji} {time_str}\n\n"

            msg_text = get_text(lang, 'message_text', 'all_time_booked') + "\n\n" + all_time
            await bot.send_message(chat_id=user_id, text=msg_text)
            await state.set_state(statuslar.orderhistory)
        else:
            await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'noorders'),
                                   reply_markup=kb.back(lang))
            await state.set_state(statuslar.orderhistory)

    elif message.text == get_text(lang, "buttons", "cancel_booking"):
        # Jarayonda bo'lgan vaqtlarni ajratib olish
        times = booking_history_user(user_id)
        ongoing_times = [time for time in times if datetime.strptime(time, "%Y-%m-%d %H:%M") >= datetime.now()]

        if ongoing_times:
            # Klaviatura yaratish
            keyboard = kb.book_time_and_dates(lang, ongoing_times)
            msg_text = get_text(lang, 'message_text', 'choose_time_cancel')  # "❌ Buyurtmani bekor qilish"
            await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'noorder_user'),reply_markup=kb.back(lang))
        await state.set_state(statuslar.orderhistory_back)



cancel_list_time = []
@router.message(statuslar.orderhistory_back)
async def back_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'history'),
                               reply_markup=kb.history(lang))
        await state.set_state(statuslar.orderhistory)
    elif message.text.startswith("⌛ "):
        cancel_list_time.append(message.text)
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'description_cancel'),reply_markup=ReplyKeyboardRemove())
        await state.set_state(statuslar.description_cancel)


@router.message(statuslar.change_language)
async def change_lang_and_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    l_list = {"🇺🇸 eng","🇺🇿 uz","🇷🇺 ru"}
    if message.text in l_list:
        for i in l_list:
            if message.text == i:
                await state.update_data(language=message.text)
                update_user_lang(user_id, message.text)
                await bot.send_message(chat_id=user_id, text=get_text(message.text, 'message_text', 'main_menu_text'),reply_markup=kb.menu(message.text))
                await state.set_state(statuslar.menu)
                break
    else:
        data = await state.get_data()
        lang = data['language']
        if message.text == get_text(lang, "buttons", "back"):
            await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb.menu(lang))
            await state.set_state(statuslar.menu)



@router.message(statuslar.location)
async def back_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu(lang))
        await state.set_state(statuslar.menu)



@router.message(statuslar.barber_contact)
async def back_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu(lang))
        await state.set_state(statuslar.menu)



@router.message(statuslar.book_barber)
async def barber_book(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu(lang))
        await state.set_state(statuslar.menu)
    elif message.text == get_text(lang, "buttons", "today"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'today_book'),reply_markup=kb.book_time(lang))
        await state.set_state(statuslar.conf_time)
    elif message.text == get_text(lang, "buttons", "another_day"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'today_book'),
                               reply_markup=kb.test_month(lang))
        await state.set_state(statuslar.test_month)


dates = []
@router.message(statuslar.test_month)
async def confirmation_time(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    another_day = message.text.split(" ")
    if another_day[0].startswith("🗒") and another_day[1][:2].isdigit() and another_day[2] == '-' and another_day[3].isalpha():
        dates.append(another_day[1])
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'today_book'),
                               reply_markup=kb.book_time_and_data(lang,another_day[1]))
        await state.set_state(statuslar.conf_time)
    if message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'book_barber'),reply_markup=kb.book_barber(lang))
        await state.set_state(statuslar.book_barber)



@router.message(statuslar.conf_time)
async def confirmation_time(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    text = message.text
    splt = text.split(":")
    if text.startswith("⏱️") and splt[1].isdigit():
        if len(dates) == 1:
            msg_text = (
                f"{get_text(lang, 'message_text', 'conf_time')}\n🗓 {dates[0] + '-' + str(datetime.today().date())[:4]}\n{message.text}"
            )
            dates.append(message.text[2:])
        else:
            dates.append(message.text[1:])
            msg_text = (
                f"{get_text(lang, 'message_text', 'conf_time')}\n{message.text}"
            )
        await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=kb.confirmation_time(lang))
        await state.set_state(statuslar.conf_time_and_menu)
    elif message.text == get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'book_barber'),reply_markup=kb.book_barber(lang))
        await state.set_state(statuslar.book_barber)



@router.message(statuslar.conf_time_and_menu)
async def confirmation_time_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "confirm"):
        if len(dates) == 1:
            # Tozalash:
            import re
            time_match = re.search(r"\d{2}:\d{2}", dates[0])
            if time_match:
                clean_time = time_match.group()
            else:
                await bot.send_message(chat_id=user_id, text="❌ Noto‘g‘ri vaqt formati!")
                return

            # Matnni formatlash
            text = get_text(lang, 'message_text', 'booked_user')
            msg_text = text.format(time=clean_time)

            times = f"{datetime.today().date()} {clean_time}"

            if booked_time(str(user_id), times, 1):
                await bot.send_location(chat_id=user_id, latitude=41.331411, longitude=69.252588)
                await bot.send_message(chat_id=user_id, text=msg_text)
                await bot.send_message(
                    chat_id=user_id,
                    text=get_text(lang, 'message_text', 'main_menu_text'),
                    reply_markup=kb.menu(lang)
                )
                await state.set_state(statuslar.menu)
                dates.clear()

        else:
            text = get_text(lang, 'message_text', 'booked_user')
            msg_text = (
                f"{text.replace("00:00", f"\n🗒 {dates[0]}\n ⏱️ {dates[1]}")}"
            )
            day = dates[0].split("-")
            times = str(datetime.today().date())[:4] + "-" + day[1] + "-" + day[0] + dates[1]
            if booked_time(user_id,  times, 1):
                await bot.send_location(chat_id=user_id, latitude=41.331411, longitude=69.252588)
                await bot.send_message(chat_id=user_id, text=msg_text)
                await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'main_menu_text'),
                                       reply_markup=kb.menu(lang))
                await state.set_state(statuslar.menu)
                dates.clear()

