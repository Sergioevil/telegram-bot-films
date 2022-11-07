from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMedia, InputMediaPhoto
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import input_media
from aiogram.utils.exceptions import MessageNotModified, Throttled
from config import TOKEN
import re
import json
import parse
import requests
import asyncio


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
		
inline_btn_1 = InlineKeyboardButton('Поиск по названию', callback_data='search')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')

backbtn1 = InlineKeyboardButton('Назад', callback_data='back')
backbtn = InlineKeyboardMarkup().add(backbtn1)

inline_kb_full = InlineKeyboardMarkup().add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('🔥 Фильмы', callback_data='films'))
# inline_kb_full.add(InlineKeyboardButton('🔥 Trending', callback_data='films'))
# inline_kb_full.add(InlineKeyboardButton('🔥 What\'s Popular?', callback_data='films'))


firstplayerbtns1 = InlineKeyboardButton('Меню', callback_data='back')
firstplayerbtns2 = InlineKeyboardButton('➡️', callback_data='next')

middleplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='previous')
middleplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
middleplayerbtns3 = InlineKeyboardButton('➡️', callback_data='next')

lastplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='previous')
lastplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')

toseekeyboardbtns1 = InlineKeyboardButton('Меню', callback_data='back')

user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4433.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/89.0.4389.114 Safari/537.36'
]

@dp.message_handler(commands=['start', 'back'])
async def process_start_command(msg: types.Message):
    global message1, message2, photos_message, photos_caption_message
    try:
        await message2.delete()
        del message2
    except:
        pass
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await asyncio.wait([i.delete() for i in photos_message])
        del photos_message
    except:
        pass
    try:
        await photos_caption_message.delete()
        del photos_caption_message
    except:
        pass
    message1 = await bot.send_message(msg.chat.id, '<b>📃 Главное меню</b>', reply_markup=inline_kb_full, parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data == 'search')
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global message1
    try:
        await message1.delete()
        del message1
    except:
        pass
    message1 = await bot.send_message(callback_query.message.chat.id, 'Напишите название фильма, а я постараюсь его найти', reply_markup=backbtn)


@dp.message_handler(commands=['films'])
async def films_command(msg: types.Message):
    global countofmovie, data, message2, photos_message, photos_caption_message, message1
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await message2.delete()
        del message2
    except:
        pass
    message3 = await bot.send_message(msg.chat.id, 'Поиск...')
    data = parse.best_movies(user_agents)
    await message3.delete()
    del message3
    countofmovie = 1
    caption = f"""Вернуться в главное меню - /back"""
    
    media = types.MediaGroup()
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6].get('img_link'), caption=f"1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+1].get('img_link'), caption=f"2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+2].get('img_link'), caption=f"3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+3].get('img_link'), caption=f"4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+4].get('img_link'), caption=f"5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+5].get('img_link'), caption=f"6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}"))
    photos_message = await bot.send_media_group(msg.chat.id, media=media)
    button_choose_1 = InlineKeyboardButton(f"""1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}""", callback_data="cho_1")
    button_choose_2 = InlineKeyboardButton(f"""2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}""", callback_data="cho_2")
    button_choose_3 = InlineKeyboardButton(f"""3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}""", callback_data="cho_3")
    button_choose_4 = InlineKeyboardButton(f"""4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}""", callback_data="cho_4")
    button_choose_5 = InlineKeyboardButton(f"""5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}""", callback_data="cho_5")
    button_choose_6 = InlineKeyboardButton(f"""6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}""", callback_data="cho_6")
    inl_keyboard_choose = InlineKeyboardMarkup().add(button_choose_1).add(button_choose_2).add(button_choose_3).add(button_choose_4).add(button_choose_5).add(button_choose_6)
    inl_keyboard_choose.add(InlineKeyboardButton("⤵️ | Загрузить ещё... | ⤵️", callback_data='load_more'))
    photos_caption_message = await bot.send_message(msg.chat.id, caption, reply_markup=inl_keyboard_choose)



@dp.callback_query_handler(lambda c: c.data == 'films')
async def films(callback_query: types.CallbackQuery):
    global countofmovie, data, message2, photos_message, photos_caption_message, message1
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await message2.delete()
        del message2
    except:
        pass
    message3 = await bot.send_message(callback_query.message.chat.id, 'Поиск...')
    data = parse.best_movies(user_agents)
    await message3.delete()
    del message3
    countofmovie = 1
    caption = f"""Вернуться в главное меню - /back"""
    
    media = types.MediaGroup()
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6].get('img_link'), caption=f"1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+1].get('img_link'), caption=f"2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+2].get('img_link'), caption=f"3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+3].get('img_link'), caption=f"4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+4].get('img_link'), caption=f"5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+5].get('img_link'), caption=f"6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}"))
    photos_message = await bot.send_media_group(callback_query.message.chat.id, media=media)
    button_choose_1 = InlineKeyboardButton(f"""1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}""", callback_data="cho_1")
    button_choose_2 = InlineKeyboardButton(f"""2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}""", callback_data="cho_2")
    button_choose_3 = InlineKeyboardButton(f"""3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}""", callback_data="cho_3")
    button_choose_4 = InlineKeyboardButton(f"""4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}""", callback_data="cho_4")
    button_choose_5 = InlineKeyboardButton(f"""5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}""", callback_data="cho_5")
    button_choose_6 = InlineKeyboardButton(f"""6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}""", callback_data="cho_6")
    inl_keyboard_choose = InlineKeyboardMarkup().add(button_choose_1).add(button_choose_2).add(button_choose_3).add(button_choose_4).add(button_choose_5).add(button_choose_6)
    inl_keyboard_choose.add(InlineKeyboardButton("⤵️ | Загрузить ещё... | ⤵️", callback_data='load_more'))
    photos_caption_message = await bot.send_message(callback_query.message.chat.id, caption, reply_markup=inl_keyboard_choose)


@dp.callback_query_handler(lambda c: c.data == 'load_more')
async def load_more(callback_query: types.CallbackQuery):
    global countofmovie, data, message2, message1, photos_message, photos_caption_message
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await message2.delete()
        del message2
    except:
        pass
    try:
        await asyncio.wait([i.delete() for i in photos_message])
        del photos_message
    except:
        pass
    try:
        await photos_caption_message.delete()
        del photos_caption_message
    except:
        pass
    countofmovie += 1
    caption = f"""Вернуться в главное меню - /back"""
    media = types.MediaGroup()
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6].get('img_link'), caption=f"1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+1].get('img_link'), caption=f"2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+2].get('img_link'), caption=f"3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+3].get('img_link'), caption=f"4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+4].get('img_link'), caption=f"5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+5].get('img_link'), caption=f"6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}"))
    photos_message = await bot.send_media_group(callback_query.message.chat.id, media=media)
    button_choose_1 = InlineKeyboardButton(f"""1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}""", callback_data="cho_1")
    button_choose_2 = InlineKeyboardButton(f"""2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}""", callback_data="cho_2")
    button_choose_3 = InlineKeyboardButton(f"""3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}""", callback_data="cho_3")
    button_choose_4 = InlineKeyboardButton(f"""4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}""", callback_data="cho_4")
    button_choose_5 = InlineKeyboardButton(f"""5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}""", callback_data="cho_5")
    button_choose_6 = InlineKeyboardButton(f"""6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}""", callback_data="cho_6")
    
    inl_keyboard_choose = InlineKeyboardMarkup()
    inl_keyboard_choose.add(InlineKeyboardButton("⤴️ | Показать предыдущие | ⤴️", callback_data='load_more_up'))
    inl_keyboard_choose.add(button_choose_1).add(button_choose_2).add(button_choose_3).add(button_choose_4).add(button_choose_5).add(button_choose_6)
    inl_keyboard_choose.add(InlineKeyboardButton("⤵️ | Загрузить ещё... | ⤵️", callback_data='load_more'))
    photos_caption_message = await bot.send_message(callback_query.message.chat.id, caption, reply_markup=inl_keyboard_choose)


@dp.callback_query_handler(lambda c: c.data == 'load_more_up')
async def load_more_up(callback_query: types.CallbackQuery):
    global countofmovie, data, message2, message1, photos_message, photos_caption_message
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await message2.delete()
        del message2
    except:
        pass
    try:
        await asyncio.wait([i.delete() for i in photos_message])
        del photos_message
    except:
        pass
    try:
        await photos_caption_message.delete()
        del photos_caption_message
    except:
        pass
    countofmovie -= 1
    caption = f"""Вернуться в главное меню - /back"""
    media = types.MediaGroup()
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6].get('img_link'), caption=f"1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+1].get('img_link'), caption=f"2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+2].get('img_link'), caption=f"3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+3].get('img_link'), caption=f"4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+4].get('img_link'), caption=f"5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}"))
    media.attach_photo(InputMediaPhoto(data[(countofmovie-1)*6+5].get('img_link'), caption=f"6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}"))
    photos_message = await bot.send_media_group(callback_query.message.chat.id, media=media)
    button_choose_1 = InlineKeyboardButton(f"""1. {data[(countofmovie-1)*6].get('title')} {data[(countofmovie-1)*6].get('film_quality')+' ' if data[(countofmovie-1)*6].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6].get('description'))}""", callback_data="cho_1")
    button_choose_2 = InlineKeyboardButton(f"""2. {data[(countofmovie-1)*6+1].get('title')} {data[(countofmovie-1)*6+1].get('film_quality')+' ' if data[(countofmovie-1)*6+1].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+1].get('description'))}""", callback_data="cho_2")
    button_choose_3 = InlineKeyboardButton(f"""3. {data[(countofmovie-1)*6+2].get('title')} {data[(countofmovie-1)*6+2].get('film_quality')+' ' if data[(countofmovie-1)*6+2].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+2].get('description'))}""", callback_data="cho_3")
    button_choose_4 = InlineKeyboardButton(f"""4. {data[(countofmovie-1)*6+3].get('title')} {data[(countofmovie-1)*6+3].get('film_quality')+' ' if data[(countofmovie-1)*6+3].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+3].get('description'))}""", callback_data="cho_4")
    button_choose_5 = InlineKeyboardButton(f"""5. {data[(countofmovie-1)*6+4].get('title')} {data[(countofmovie-1)*6+4].get('film_quality')+' ' if data[(countofmovie-1)*6+4].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+4].get('description'))}""", callback_data="cho_5")
    button_choose_6 = InlineKeyboardButton(f"""6. {data[(countofmovie-1)*6+5].get('title')} {data[(countofmovie-1)*6+5].get('film_quality')+' ' if data[(countofmovie-1)*6+5].get('film_quality') else ''}{' '.join(data[(countofmovie-1)*6+5].get('description'))}""", callback_data="cho_6")
    inl_keyboard_choose = InlineKeyboardMarkup()
    if countofmovie != 1:
        inl_keyboard_choose.add(InlineKeyboardButton("⤴️ | Показать предыдущие | ⤴️", callback_data='load_more_up'))
    inl_keyboard_choose.add(button_choose_1).add(button_choose_2).add(button_choose_3).add(button_choose_4).add(button_choose_5).add(button_choose_6)
    inl_keyboard_choose.add(InlineKeyboardButton("⤵️ | Загрузить ещё... | ⤵️", callback_data='load_more'))
    photos_caption_message = await bot.send_message(callback_query.message.chat.id, caption, reply_markup=inl_keyboard_choose)


@dp.callback_query_handler(lambda c: c.data == 'cho_1')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6].get('link')) 
    if len(seasons) == 0:    
        toseefirstplayerbtns1 = InlineKeyboardButton('Меню', callback_data='back')
        toseefirstplayerbtns2 = InlineKeyboardButton('➡️', callback_data='cho_2')
        toseefirstplayer = InlineKeyboardMarkup(row_width=2)
        toseefirstplayer.row(toseefirstplayerbtns1,toseefirstplayerbtns2)
        toseefirstplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseefirstplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseefirstplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"1. {data[(countofmovie-1)*6].get('title')}"+f"""    {data[(countofmovie-1)*6].get('film_quality') if data[(countofmovie-1)*6].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6].get('description'))
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6].get('img_link'), caption=caption), reply_markup=toseefirstplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6].get('img_link')).content,
                caption=caption,
                reply_markup=toseefirstplayer)


@dp.callback_query_handler(lambda c: c.data == 'cho_2')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6+1].get('link')) 
    if len(seasons) == 0: 
        toseemiddleplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='cho_1')
        toseemiddleplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
        toseemiddleplayerbtns3 = InlineKeyboardButton('➡️', callback_data='cho_3')
        toseemiddleplayer = InlineKeyboardMarkup(row_width=3)
        toseemiddleplayer.row(toseemiddleplayerbtns1,toseemiddleplayerbtns2,toseemiddleplayerbtns3)
        toseemiddleplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseemiddleplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseemiddleplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"2. {data[(countofmovie-1)*6+1].get('title')}"+f"""    {data[(countofmovie-1)*6+1].get('film_quality') if data[(countofmovie-1)*6+1].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6+1].get('description'))    
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6+1].get('img_link'), caption=caption), reply_markup=toseemiddleplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6+1].get('img_link')).content,
                caption=caption,
                reply_markup=toseemiddleplayer)


@dp.callback_query_handler(lambda c: c.data == 'cho_3')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6+2].get('link')) 
    if len(seasons) == 0: 
        toseemiddleplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='cho_2')
        toseemiddleplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
        toseemiddleplayerbtns3 = InlineKeyboardButton('➡️', callback_data='cho_4')
        toseemiddleplayer = InlineKeyboardMarkup(row_width=3)
        toseemiddleplayer.row(toseemiddleplayerbtns1,toseemiddleplayerbtns2,toseemiddleplayerbtns3)
        toseemiddleplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseemiddleplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseemiddleplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"3. {data[(countofmovie-1)*6+2].get('title')}"+f"""    {data[(countofmovie-1)*6+2].get('film_quality') if data[(countofmovie-1)*6+2].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6+2].get('description'))    
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6+2].get('img_link'), caption=caption), reply_markup=toseemiddleplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6+2].get('img_link')).content,
                caption=caption,
                reply_markup=toseemiddleplayer)


@dp.callback_query_handler(lambda c: c.data == 'cho_4')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6+3].get('link')) 
    if len(seasons) == 0: 
        toseemiddleplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='cho_3')
        toseemiddleplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
        toseemiddleplayerbtns3 = InlineKeyboardButton('➡️', callback_data='cho_5')
        toseemiddleplayer = InlineKeyboardMarkup(row_width=3)
        toseemiddleplayer.row(toseemiddleplayerbtns1,toseemiddleplayerbtns2,toseemiddleplayerbtns3)
        toseemiddleplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseemiddleplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseemiddleplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"4. {data[(countofmovie-1)*6+3].get('title')}"+f"""    {data[(countofmovie-1)*6+3].get('film_quality') if data[(countofmovie-1)*6+3].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6+3].get('description'))    
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6+3].get('img_link'), caption=caption), reply_markup=toseemiddleplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6+3].get('img_link')).content,
                caption=caption,
                reply_markup=toseemiddleplayer)


@dp.callback_query_handler(lambda c: c.data == 'cho_5')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6+4].get('link')) 
    if len(seasons) == 0: 
        toseemiddleplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='cho_4')
        toseemiddleplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
        toseemiddleplayerbtns3 = InlineKeyboardButton('➡️', callback_data='cho_6')
        toseemiddleplayer = InlineKeyboardMarkup(row_width=3)
        toseemiddleplayer.row(toseemiddleplayerbtns1,toseemiddleplayerbtns2,toseemiddleplayerbtns3)
        toseemiddleplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseemiddleplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseemiddleplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"5. {data[(countofmovie-1)*6+4].get('title')}"+f"""    {data[(countofmovie-1)*6+4].get('film_quality') if data[(countofmovie-1)*6+4].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6+4].get('description'))
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6+4].get('img_link'), caption=caption), reply_markup=toseemiddleplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6+4].get('img_link')).content,
                caption=caption,
                reply_markup=toseemiddleplayer)


@dp.callback_query_handler(lambda c: c.data == 'cho_6')
async def first(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    video_link, descrip, seasons, eps = parse.get_video_link(data[(countofmovie-1)*6+5].get('link')) 
    if len(seasons) == 0: 
        toseelastplayerbtns1 = InlineKeyboardButton('⬅️', callback_data='cho_5')
        toseelastplayerbtns2 = InlineKeyboardButton('Меню', callback_data='back')
        toseelastplayer = InlineKeyboardMarkup(row_width=2)
        toseelastplayer.row(toseelastplayerbtns1,toseelastplayerbtns2)
        toseelastplayer.add(InlineKeyboardButton('Смотреть', url=video_link))
    else:
        toseelastplayer = InlineKeyboardMarkup()
        for s in seasons:
            toseelastplayer.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
    caption = f"6. {data[(countofmovie-1)*6+5].get('title')}"+f"""    {data[(countofmovie-1)*6+5].get('film_quality') if data[(countofmovie-1)*6+5].get('film_quality') else ''}\n\n"""+descrip+'\n\n'+'        '.join(data[(countofmovie-1)*6+5].get('description'))
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    try:
        await message1.edit_media(InputMediaPhoto(media=data[(countofmovie-1)*6+5].get('img_link'), caption=caption), reply_markup=toseelastplayer)
    except:
        try:
            if message1:
                pass
        except:
            message1 = await bot.send_photo(
                chat_id = callback_query.message.chat.id, 
                photo = requests.get(data[(countofmovie-1)*6+5].get('img_link')).content,
                caption=caption,
                reply_markup=toseelastplayer)


@dp.callback_query_handler(lambda c: c.data == 'back')
async def tomainmenu(callback_query: types.CallbackQuery):
    global message1, message2, photos_message, photos_caption_message
    try:
        await message2.delete()
        del message2
    except:
        pass
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await asyncio.wait([i.delete() for i in photos_message])
        del photos_message
    except:
        pass
    try:
        await photos_caption_message.delete()
        del photos_caption_message
    except:
        pass
    message1 = await bot.send_message(callback_query.message.chat.id, 'Главное меню', reply_markup=inline_kb_full)


# __________ search module __________
@dp.message_handler()
async def process_start_command(msg: types.Message):
    global countofmovie, data, message2, message1
    try:
        await message1.delete()
        del message1
    except:
        pass
    try:
        await message2.delete()
        del message2
    except:
        pass
    message3 = await bot.send_message(msg.chat.id, 'Поиск...')
    data = parse.search_result_afdah(str(msg.text), user_agents)
    await message3.delete()
    del message3
    if len(data) == 0:
        message2 = await bot.send_message(msg.chat.id, 'Результатов не найдено', reply_markup=backbtn)
        return
    elif len(data) == 1:
        message2 = await bot.send_message(msg.chat.id, f'Найден {len(data)} фильм')
    elif len(data) > 1 and len(data) <= 4:
        message2 = await bot.send_message(msg.chat.id, f'Найдено {len(data)} фильма')
    elif len(data) > 4 and len(data) <= 20:
        message2 = await bot.send_message(msg.chat.id, f'Найдено {len(data)} фильмов')
    else:
        message2 = await bot.send_message(msg.chat.id, f'Найдено более 20 фильмов')
    firstplayer = InlineKeyboardMarkup(row_width=2)
    firstplayer.row(firstplayerbtns1,firstplayerbtns2)
    firstplayer.add(InlineKeyboardButton('Выбрать', callback_data="choose"))
    countofmovie = 1
    caption = f"{countofmovie}. {data[0].get('title')}"+f"""{'''

Качество: '''+data[0].get('film_quality') if data[0].get('film_quality') else ''}\n\n"""+'    '.join(data[0].get('description'))
    message1 = await bot.send_photo(
        chat_id = msg.from_user.id, 
        photo = requests.get(data[0].get('img_link')).content,
        caption=caption,
        reply_markup=firstplayer)


@dp.callback_query_handler(lambda c: c.data == 'next')
async def tonextmovie(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    countofmovie += 1
    caption = f"{countofmovie}. {data[countofmovie-1].get('title')}"+f"""{'''

Качество: '''+data[countofmovie-1].get('film_quality') if data[countofmovie-1].get('film_quality') else ''}\n\n"""+'    '.join(data[countofmovie-1].get('description'))
    try:
        if countofmovie == len(data):
            lastplayer = InlineKeyboardMarkup(row_width=2)
            lastplayer.row(lastplayerbtns1,lastplayerbtns2)
            lastplayer.add(InlineKeyboardButton('Выбрать', callback_data="choose"))
            await message1.edit_media(InputMediaPhoto(media=data[countofmovie-1].get('img_link'), caption=caption), reply_markup=lastplayer)
        elif countofmovie < len(data):
            middleplayer = InlineKeyboardMarkup(row_width=3)
            middleplayer.row(middleplayerbtns1,middleplayerbtns2,middleplayerbtns3)
            middleplayer.add(InlineKeyboardButton('Выбрать', callback_data="choose"))
            await message1.edit_media(InputMediaPhoto(media=data[countofmovie-1].get('img_link'), caption=caption), reply_markup=middleplayer)
    except:
        await bot.send_message(callback_query.message.chat.id, "Что-то пошло не так...")


@dp.callback_query_handler(lambda c: c.data == 'previous')
async def previous(callback_query: types.CallbackQuery):
    global countofmovie, data, message1
    countofmovie -= 1
    caption = f"{countofmovie}. {data[countofmovie-1].get('title')}"+f"""{'''

Качество: '''+data[countofmovie-1].get('film_quality') if data[countofmovie-1].get('film_quality') else ''}\n\n"""+'    '.join(data[countofmovie-1].get('description'))
    if countofmovie == 1:
        firstplayer = InlineKeyboardMarkup(row_width=2)  #.add(firstplayerbtns1).add(firstplayerbtns2)
        firstplayer.row(firstplayerbtns1,firstplayerbtns2)
        firstplayer.add(InlineKeyboardButton('Выбрать', callback_data="choose"))
        await message1.edit_media(InputMediaPhoto(media=data[countofmovie-1].get('img_link'), caption=caption),reply_markup=firstplayer)
    else:
        middleplayer = InlineKeyboardMarkup(row_width=3)
        middleplayer.row(middleplayerbtns1,middleplayerbtns2,middleplayerbtns3)
        middleplayer.add(InlineKeyboardButton('Выбрать', callback_data="choose"))
        await message1.edit_media(InputMediaPhoto(media=data[countofmovie-1].get('img_link'), caption=caption),reply_markup=middleplayer)


@dp.callback_query_handler(lambda c: c.data == 'choose')
async def choose(callback_query: types.CallbackQuery):
    global countofmovie, data, message1, seasons, eps, video_link
    video_link, description, seasons, eps = parse.get_video_link(data[countofmovie-1].get('link')) 
    if len(seasons) == 0:
        toseekeyboard = InlineKeyboardMarkup()
        toseekeyboard.row(toseekeyboardbtns1)
        toseekeyboard.add(InlineKeyboardButton('Смотреть', url=video_link))
        caption = f"{countofmovie}. {data[countofmovie-1].get('title')}"+f"""{'''

Качество: '''+data[countofmovie-1].get('film_quality') if data[countofmovie-1].get('film_quality') else ''}\n\n"""+'    '.join(data[countofmovie-1].get('description'))
    else:
        toseekeyboard = InlineKeyboardMarkup()
        for s in seasons:
            toseekeyboard.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
        # print(seasons)
        # print(eps)
        caption = f"{countofmovie}. {data[countofmovie-1].get('title')}"+f"""{'''

Качество: '''+data[countofmovie-1].get('film_quality') if data[countofmovie-1].get('film_quality') else ''}\n\n"""+'    '.join(data[countofmovie-1].get('description'))+'\n\n'+"Вернуться в главное меню - /back"

    await message1.edit_caption(caption=caption,reply_markup=toseekeyboard)


@dp.callback_query_handler(lambda c: 'season_' in c.data)
async def season(callback_query: types.CallbackQuery):
    global message1, seasons, eps, video_link, season_index
    try:
        if season_index == int(callback_query.data.replace('season_', '')):
            await bot.answer_callback_query(callback_query.id, show_alert=False)
            return
    except:
        pass
    season_index = int(callback_query.data.replace('season_', ''))
    tosee_epskeyboard = InlineKeyboardMarkup()
    for s in seasons:
        tosee_epskeyboard.add(InlineKeyboardButton(s, callback_data=f"season_{seasons.index(s)}"))
        if season_index == seasons.index(s):
            temp_5 = []
            counter = 0
            for e in eps[season_index]:
                counter+=1
                but = InlineKeyboardButton(e, url=re.sub(r"&s=\d\d?&e=\d\d?\d?", f"&s={season_index+1}&e={e}", video_link))
                temp_5.append(but)
                if counter == 5:
                    tosee_epskeyboard.row(*temp_5)
                    temp_5 = []
                    counter = 0
            if len(temp_5) != 0:
                if len(temp_5) == 1:
                    tosee_epskeyboard.add(*temp_5)
                else:
                    tosee_epskeyboard.row(*temp_5)

    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await message1.edit_reply_markup(reply_markup=tosee_epskeyboard)


@dp.errors_handler()
async def message_not_modified_handler(update, error):
    try:
        await bot.send_message(update.callback_query.message.chat.id, 'Обновите бота - /start')
    except:
        pass
    return True # errors_handler must return True if error was handled correctly


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)