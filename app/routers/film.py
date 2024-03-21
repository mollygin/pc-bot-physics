from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from typing import Union

from ..data import (
    get_films,
    get_film,
    save_film
)
from ..keyboards import (
    build_films_keyboard,
    build_film_details_keyboard,
    build_menu_keyboard
)
from ..fsm import FilmCreateForm

film_router = Router()

#Buttons
@film_router.message(Command("formulas"))
@film_router.message(F.text.casefold() == "formulas")
async def show_films_command(message: Message, state: FSMContext) -> None:
    keyboard1 = build_menu_keyboard()
    await message.answer("Choose an option:", reply_markup=keyboard1)
    films = get_films()
    keyboard = build_films_keyboard(films)
    #message:
    await message.answer(
        text="Виберіть свій клас: ",
        reply_markup=keyboard
    )

# from aiogram.utils.markdown import hbold
@film_router.callback_query(F.data.startswith("film_"))
async def show_film_details(callback: CallbackQuery, state: FSMContext) -> None:
    film_id = int(callback.data.split("_")[-1])
    film = get_film(film_id)
    text = (f"Ваш клас: {hbold(film.get('title'))}\n")
    photo_id = film.get('photo')
    for photo in photo_id:
        await callback.message.answer_photo(photo)

    url = film.get('url')
    await edit_or_answer(callback.message, text, build_film_details_keyboard(url))

async def edit_or_answer(message: Message, text: str, keyboard, *args, **kwargs):
    if message.from_user.is_bot:
        await message.edit_text(text=text, reply_markup=keyboard, **kwargs)
    else:
        await message.answer(text=text, reply_markup=keyboard, **kwargs)





@film_router.message(Command("createform"))
@film_router.message(F.text.casefold() == "createform")
@film_router.message(F.text.casefold() == "create formula")
async def create_film_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(FilmCreateForm.title)
    await edit_or_answer(message, "Назва класу/формул: ", ReplyKeyboardRemove())

@film_router.message(FilmCreateForm.title)
async def proces_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    data = await state.update_data(desc=message.text)
    await state.set_state(FilmCreateForm.url)
    await edit_or_answer(
        message,
        f"Ссилка на формули: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )

@film_router.message(FilmCreateForm.url)
@film_router.message(F.text.contains("http"))
async def proces_url(message: Message, state: FSMContext) -> None:
    data = await state.update_data(url=message.text)
    await state.set_state(FilmCreateForm.photo)
    await edit_or_answer(
        message,f"Фотографії: {hbold(data.get('title'))}", ReplyKeyboardRemove(),)

@film_router.message(FilmCreateForm.photo)
@film_router.message(F.photo)
async def proces_photo(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    photo_id = photo.file_id
    data = await state.update_data(photo=photo_id)
    await state.clear()
    save_film(data)
    return await show_films_command(message, state)

@film_router.callback_query(F.data == "back")
@film_router.message(Command("back"))
async def back_handler(callback: Union[CallbackQuery, Message], state: FSMContext) -> None:
    await state.clear()
    return await show_films_command(callback.message, state)