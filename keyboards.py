from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Harry Potter')
b2 = KeyboardButton('Something else (not working)')
# b3 = KeyboardButton('Выполненные дела')
b4 = KeyboardButton('/start')
kb_start.add(b1).insert(b2)


kb_ml = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/cancel')
kb_ml.add(b1)