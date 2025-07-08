import json
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from api import create_user,check_userid,check_admin
from decouple import config

# local modules
import keyboards as kb
from stateall import statuslar


TOKEN = config('TOKEN')



bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
choosed_lang = {}


with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")



@router.message(F.text.startswith("/start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = check_userid(user_id)
    admin = check_admin(user_id)  # [123123,123123123]
    if user:
        lang = "🇺🇿 uz" if user['lang'] == "uz" else "🇷🇺 ru" if user['lang'] == 'ru' else '🇺🇸 en'
        if user_id not in admin:
            await message.answer(text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu(lang))
            await state.set_state(statuslar.main_menu)
        else:
            await message.answer(text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu_admin(lang))
            await state.set_state(statuslar.main_menu)

    else:
        await message.answer(text=translations['start'], reply_markup=kb.start_key(),parse_mode='HTML')
        await state.set_state(statuslar.language)




@router.message(statuslar.language)
async def ask_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id


    # if user:
    #     if user_id not in admin:
    #         await message.answer(text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu(lang))
    #         await state.set_state(statuslar.main_menu)
    #     else:
    #         await message.answer(text=get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb.menu_admin(lang))
    #         await state.set_state(statuslar.main_menu)
    #
    # else:
    if message.text in ["🇺🇸 eng","🇺🇿 uz","🇷🇺 ru"]:
        await state.update_data(name=message.text)
        data = await state.get_data()
        lang = data['name']
        await message.answer(text=get_text(lang, 'message_text', 'contact'),reply_markup=kb.phone_key(lang))
        await state.set_state(statuslar.phone)
    else:
        pass




@router.message(statuslar.phone)
async def check_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['name']
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await message.answer(text=get_text(lang, 'message_text', 'user_info'), reply_markup=kb.back(lang))
        await state.set_state(statuslar.fio)
    else:
        text = message.text
        if message.text.startswith("+998") and len(text) == 13 and text[1:].isdigit():
            await state.update_data(phone=message.text)
            await message.answer(text=get_text(lang, 'message_text', 'user_info'), reply_markup=kb.back(lang))
            await state.set_state(statuslar.fio)
        else:
            await message.answer(text=get_text(lang, 'message_text', 'error_phone'))



@router.message(statuslar.fio)
async def fio_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['name']
    ok = True
    if message.text == get_text(lang, 'buttons', 'back'):
        await message.answer(text=get_text(lang, 'message_text', 'contact'), reply_markup=kb.phone_key(lang))
        await state.set_state(statuslar.phone)
    else:
        for i in message.text:
            if not i.isalpha():
                await message.answer(text=get_text(lang, 'message_text', 'error_name'))
                ok = False
        if ok:
            await state.update_data(user_name=message.text)
            msg_text = (
                f"{get_text(lang, 'message_text', 'show_info')}\n\n"
                f"{get_text(lang, 'message_text', 'phone')} {data["phone"]}\n"
                f"{get_text(lang, 'message_text', 'name')} {message.text}"
            )
            await message.answer(text=msg_text, reply_markup=kb.conf(lang))
            await state.set_state(statuslar.con_rej)




@router.message(statuslar.con_rej)
async def check_info(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['name']
    if message.text == get_text(lang, 'buttons', 'confirm'):
        response = create_user(data["phone"], data["user_name"], user_id, lang)
        if response:
            await message.answer(text=get_text(lang, 'message_text', 'conf_text'), reply_markup=kb.menu(lang))
            await state.set_state(statuslar.main_menu)
        else:
            await message.answer(text=get_text(lang, 'message_text', '400'))
    elif message.text == get_text(lang, 'buttons', 'rejected'):
        await message.answer(text=translations['start'], reply_markup=kb.start_key(), parse_mode='HTML')
        await state.set_state(statuslar.language)



@router.message(statuslar.con_rej)
async def check_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['name']

