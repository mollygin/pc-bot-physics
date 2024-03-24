from aiogram.fsm.state import State, StatesGroup

class FilmCreateForm(StatesGroup):
    title = State()
    url = State()
    desc = State()
    photo = State()
