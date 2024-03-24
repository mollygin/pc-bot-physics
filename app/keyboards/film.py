from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
def build_films_keyboard(films: list):
    builder = InlineKeyboardBuilder()
    for index, film in enumerate(films):
        builder.button(text=film.get("title"),
                        callback_data=f"film_{index}")
    return builder.as_markup()

def build_film_details_keyboard(url):
    builder = InlineKeyboardBuilder()
    builder.button(text="Посилання на сайт: ", url=url)
    builder.button(text="Назад", callback_data="back")
    #builder.button(text="Сайт з формулами: ", url="https://brain-school.com.ua/category/formuly-fizyka/")
    return builder.as_markup()

def build_menu_keyboard():
    builder = ReplyKeyboardMarkup()
    builder.button(text="Посилання на сайт: ", callback_data="https://brain-school.com.ua/category/formuly-fizyka/")
    builder.button(text="Формули", callback_data=f"/formulas")
    builder.button(text="Створити нову формулу", callback_data=f"/createform")
    return builder.as_markup()