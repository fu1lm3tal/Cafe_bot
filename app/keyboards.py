from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import models as db

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')],
                                     [KeyboardButton(text='Заказ')]])


async def get_menu():
    categories = await db.get_category()
    menu_kb = InlineKeyboardBuilder()
    for category in categories:
        menu_kb.add(InlineKeyboardButton(text=category, callback_data=f"category_{category}"))
    return menu_kb.adjust(2).as_markup()


async def get_items(name):
    items = await db.get_items(name)
    items_kb = InlineKeyboardBuilder()
    for item in items:
        items_kb.add(InlineKeyboardButton(text=item, callback_data=f"item_{item}"))
    return items_kb.adjust(2).as_markup()
