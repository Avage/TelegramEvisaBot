from telebot import types
from src.utils.var_extractor import get_messages_var as msg


def send_settings(bot, db, call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'language_button'), callback_data='language'))
    keyboard.add(types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='menu'))
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'settings_message'), reply_markup=keyboard,
                     parse_mode='Markdown')


def send_language_settings(bot, db, call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('English🇬🇧', callback_data='en'),
                 types.InlineKeyboardButton('Русский🇷🇺', callback_data='ru'), row_width=2)
    keyboard.add(types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='settings'))
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'language_message'),
                     reply_markup=keyboard, parse_mode='Markdown')


def change_language(bot, db, call):
    if db.update_user_info_with_atr(call.from_user, "language", call.data):
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'language_selected_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')
