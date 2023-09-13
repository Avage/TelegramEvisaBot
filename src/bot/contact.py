from telebot import types
from src.utils import var_extractor
from src.utils.var_extractor import get_messages_var as msg


def send_help_menu(bot, db, message):
    if not db.user_exist(message.chat):
        if not db.add_user(message.from_user):
            bot.send_message(message.chat.id, msg('en', 'went_wrong_message'), parse_mode='Markdown')
            bot.send_message(var_extractor.get_env_var("ADMIN_ID"),
                             f"Error: Can't add user to database.\n\nUser: {message.chat.id}")
    faq_button = types.InlineKeyboardButton(msg(db.get_lg(message.chat), 'faq_button'), callback_data='faq')
    contact_with_admin = types.InlineKeyboardButton(msg(db.get_lg(message.chat), 'contact_admin_button'),
                                                    callback_data='contact_admin')
    back_button = types.InlineKeyboardButton(msg(db.get_lg(message.chat), 'back_button'), callback_data='menu')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(faq_button, contact_with_admin, back_button, row_width=2)
    bot.send_message(message.chat.id, msg(db.get_lg(message.chat), 'help_message'), reply_markup=keyboard,
                     parse_mode='Markdown')


def send_faq(bot, db, call):
    back_button = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='help')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(back_button, row_width=1)
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'faq_message'), reply_markup=keyboard,
                     parse_mode='Markdown')


def send_contact(bot, db, call):
    back_button = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'back_button'), callback_data='help')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(back_button, row_width=1)
    bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'contact_admin_message'),
                     reply_markup=keyboard, parse_mode='Markdown')
