from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterForm(StatesGroup):
    phone = State()


class PromocodeForm(StatesGroup):
    code = State()


class CartForm(StatesGroup):
    p_id = State()
    is_send = State()
