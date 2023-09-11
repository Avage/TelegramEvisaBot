from telebot import types
from src.utils import var_extractor
from src.utils.var_extractor import get_messages_var as msg


def send_visa_type(bot, db, call):
    button_single = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'single_button'), callback_data='single')
    button_multiple = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'multiple_button'),
                                                 callback_data='multiple')
    button_back = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='menu')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_single, button_multiple, button_back, row_width=2)
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'visa_type_message'),
                     reply_markup=keyboard, parse_mode='Markdown')


def send_visa_code(bot, db, call):
    keyboard = types.InlineKeyboardMarkup()
    for visa in var_extractor.get_config_var(call.data):
        if db.get_lg(call.from_user) == "ru":
            keyboard.add(types.InlineKeyboardButton(
                f"Длительность: {visa['duration']}, Цена: {visa['price']}💲{visa['currency']}",
                callback_data=visa["code"]))
        else:
            keyboard.add(
                types.InlineKeyboardButton(f"Duration: {visa['duration']}, Price: {visa['price']}💲{visa['currency']}",
                                           callback_data=visa["code"]))
    keyboard.add(types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='start'))
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'visa_duration_message'),
                     reply_markup=keyboard, parse_mode='Markdown')
