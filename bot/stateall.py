from aiogram.fsm.state import State, StatesGroup


class statuslar(StatesGroup):
    language = State()
    phone = State()
    fio = State()
    main_menu = State()
    con_rej = State()