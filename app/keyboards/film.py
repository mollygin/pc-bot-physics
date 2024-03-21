from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
    #builder.button(text="Сайт: ", url="https://brain-school.com.ua/category/formuly-fizyka/")
    return builder.as_markup()

def build_menu_keyboard():
    #keyboard = InlineKeyboardMarkup()
    #link_button = InlineKeyboardButton(text="Сайт з інформацією: ", url="https://brain-school.com.ua/category/formuly-fizyka/")
    #keyboard.add(link_button)
    #return keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    link_button = InlineKeyboardButton(text="Сайт з інформацією: ",
                                       url="https://brain-school.com.ua/category/formuly-fizyka/")
    keyboard.add(link_button)
    return keyboard
