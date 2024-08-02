from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app import keyboards as kb
from app.database import models as db

router = Router()


class Reg(StatesGroup):
    name = State()
    email = State()
    number = State()


@router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    user = await db.get_id(message.from_user.id)
    await message.reply('Добро пожаловать в наше кафe!', reply_markup=kb.main)
    if not user:
        await message.answer('Пожалуйста введите ваше имя')
        await state.set_state(Reg.name)


@router.message(Reg.name)
async def one_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.email)
    await message.answer('Введите ваш email')


@router.message(Reg.email)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите ваш номер телефона')


@router.message(Reg.number)
async def three_four(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await db.cmd_start_id(message.from_user.id, data["name"], data["email"], data["number"])
    await message.answer('Спасибо за регистрацию!')
    await state.clear()


@router.message(F.text == 'Меню')
async def cmd_menu(message: Message):
    await message.answer('Меню', reply_markup=await kb.get_menu())
    await kb.get_menu()
    await db.get_category()


#@router.callback_query()
#async def callback_query_handler(callback_query: CallbackQuery):
    #await callback_query.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == 'category_Напитки')
async def category_menu(query: CallbackQuery):
    await query.message.answer('Привет!')


@router.callback_query(F.data == 'category_Десерты')
async def category_menu(query: CallbackQuery):
    await query.message.answer('Как дела')


@router.callback_query(F.data == 'category_Закуски')
async def category_menu(query: CallbackQuery):
    await query.message.answer('Вы выбрали закуски', reply_markup=await kb.get_items('Закуски'))
