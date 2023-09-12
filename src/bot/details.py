from telebot import types
from src.utils import var_extractor
from src.utils.var_extractor import get_messages_var as msg


def get_name(bot, db, call):
    if call.data == "edit" and db.update_user_info_with_atr(call.from_user, "last_command", "get_name"):
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'get_name_message'),
                         parse_mode='Markdown')
    elif db.update_user_info_with_atr(call.from_user, "last_command", "get_name") and \
            db.update_user_info_with_atr(call.from_user, "visa_code", call.data):
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'get_name_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def get_last_name(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "get_last_name") and \
            db.update_user_info_with_atr(message.from_user, "passport_name", message.text):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'get_lastname_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def get_passport_number(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "get_passport_number") and \
            db.update_user_info_with_atr(message.from_user, "passport_surname", message.text):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'get_passport_number_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def get_passport_birthday(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "get_passport_birthday") and \
            db.update_user_info_with_atr(message.from_user, "passport_number", message.text):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'get_birthday_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def get_passport_photo(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "get_passport_photo") and \
            db.update_user_info_with_atr(message.from_user, "passport_birthday", message.text):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'get_passport_photo'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def get_passport_scan(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "get_passport_scan") and \
            db.update_user_info_with_atr(message.from_user, "passport_photo", message.photo[-1].file_id) and \
            db.update_user_info_with_atr(message.from_user, "passport_photo_msg_id", message.message_id):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'get_passport_scan'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def confirm_details(bot, db, message):
    if db.update_user_info_with_atr(message.from_user, "last_command", "confirm_details") and \
            db.update_user_info_with_atr(message.from_user, "passport_scan", message.photo[-1].file_id) and \
            db.update_user_info_with_atr(message.from_user, "passport_scan_msg_id", message.message_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(msg(db.get_lg(message.from_user), 'confirm_button'), callback_data='confirm'))
        keyboard.add(types.InlineKeyboardButton(msg(db.get_lg(message.from_user), 'edit_button'), callback_data='edit'))
        keyboard.add(
            types.InlineKeyboardButton(msg(db.get_lg(message.from_user), 'cancel_button'), callback_data='menu'))
        code = str(db.get_user_info_with_atr(message.from_user, "visa_code"))
        product = next(
            (dic for dic in var_extractor.get_config_var("single" if code[0] == "1" else "multiple") if
             dic['code'] == code), None)
        product_name = product["title"] + " " + str(product["price"]) + " " + product["currency"]
        name = db.get_user_info_with_atr(message.from_user, "passport_name")
        surname = db.get_user_info_with_atr(message.from_user, "passport_surname")
        number = db.get_user_info_with_atr(message.from_user, "passport_number")
        birthday = db.get_user_info_with_atr(message.from_user, "passport_birthday")
        bot.send_message(message.chat.id,
                         f"*{msg(db.get_lg(message.from_user), 'confirm_details_message')}\n\n{product_name}\n\n{name}"
                         f"\n{surname}\n{number}\n{birthday}*", reply_markup=keyboard, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def send_to_chat(bot, db, call):
    code = str(db.get_user_info_with_atr(call.from_user, "visa_code"))
    product = next(
        (dic for dic in var_extractor.get_config_var("single" if code[0] == "1" else "multiple") if
         dic['code'] == code), None)
    product_name = product["title"] + " " + str(product["price"]) + " " + product["currency"]
    name = db.get_user_info_with_atr(call.from_user, "passport_name")
    surname = db.get_user_info_with_atr(call.from_user, "passport_surname")
    number = db.get_user_info_with_atr(call.from_user, "passport_number")
    birthday = db.get_user_info_with_atr(call.from_user, "passport_birthday")
    portrait = db.get_user_info_with_atr(call.from_user, "passport_photo_msg_id")
    scan = db.get_user_info_with_atr(call.from_user, "passport_scan_msg_id")
    message_id = bot.send_message(var_extractor.get_env_var("GROUP_ID"),
                                  f"*User id - {call.from_user.id}\n\nVisa Name - {product_name}\n\nName - {name}\n"
                                  f"Surname - {surname}\nPassport Number - {number}\nBirthday - {birthday}*",
                                  parse_mode='Markdown',
                                  disable_notification=True).message_id
    fwd1_id = bot.forward_message(var_extractor.get_env_var("GROUP_ID"), call.from_user.id, portrait,
                                  disable_notification=True).message_id
    fwd2_id = bot.forward_message(var_extractor.get_env_var("GROUP_ID"), call.from_user.id, scan,
                                  disable_notification=True).message_id
    if db.update_user_info_with_atr(call.from_user, "msg_id", message_id) and \
            db.update_user_info_with_atr(call.from_user, "passport_photo_msg_id", fwd1_id) and \
            db.update_user_info_with_atr(call.from_user, "passport_scan_msg_id", fwd2_id):
        pass
    else:
        bot.send_message(var_extractor.get_env_var("ADMIN_ID"),
                         f"Error: Can't add message ids to database.\n\nUser: {call.from_user.id}")
