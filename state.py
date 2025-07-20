from aiogram.fsm.state import State, StatesGroup


class statuslar(StatesGroup):
    language = State()
    phone = State()
    fio = State()
    conf = State()
    menu = State()
    change_language = State()
    location = State()
    barber_contact = State()
    book_barber = State()
    conf_time = State()
    conf_time_and_menu = State()
    test_month = State()
    orderhistory = State()
    noorderback = State()
    orderhistory_back = State()
    description_cancel = State()
