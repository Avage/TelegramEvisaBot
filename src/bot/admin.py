from telebot import types

current_user_id = None
payment_id = None


def send_admin_menu(bot, message):
    send_visa_button = types.InlineKeyboardButton('Send Visa', callback_data='admin_send_visa')
    get_user_info_button = types.InlineKeyboardButton('Get User Info', callback_data='admin_get_user_info')
    get_payment_info_button = types.InlineKeyboardButton('Get Payment Info', callback_data='admin_get_payment_info')
    back_button = types.InlineKeyboardButton('Close Admin Panel', callback_data='menu')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(send_visa_button, get_user_info_button, get_payment_info_button, back_button, row_width=1)

    bot.send_message(message.chat.id, "*🪪🪪🪪🪪🪪🪪\n\nAdmin Panel*",
                     reply_markup=keyboard, parse_mode='Markdown')


def get_payment_id(bot, call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Back', callback_data='admin'))
    bot.send_message(call.message.chat.id, "*Send Payment ID*", parse_mode='Markdown', reply_markup=keyboard)


def get_user_id(bot, call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Back', callback_data='admin'))
    bot.send_message(call.message.chat.id, "*Send User ID*", parse_mode='Markdown', reply_markup=keyboard)


def send_visa(bot, message):
    global current_user_id
    current_user_id = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Cancel', callback_data='admin'))
    bot.send_message(message.chat.id, "*Send Visa in PDF format*", parse_mode='Markdown', reply_markup=keyboard)


def forward_to_user(bot, message):
    global current_user_id
    try:
        bot.send_message(current_user_id, "*Your visa is ready!*", parse_mode='Markdown')
        bot.forward_message(current_user_id, message.from_user.id, message.message_id)
        bot.send_message(current_user_id, "*Thank you for using our bot!*\n\n*🪪🪪🪪🪪🪪🪪*", parse_mode='Markdown')
        bot.send_message(message.chat.id, "*Visa sent successfully!*", parse_mode='Markdown')
    except Exception as err:
        print('Cause: {}'.format(err))
        bot.send_message(message.chat.id, "*Error while sending visa:\n\n{err}*", parse_mode='Markdown')


def get_user(bot, db, message):
    global current_user_id
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Back', callback_data='admin')
    keyboard.add(back_button, row_width=1)
    current_user_id = message.text
    if not db.user_exist_by_id(current_user_id):
        bot.send_message(message.chat.id, "*User Not Found*", parse_mode='Markdown', reply_markup=keyboard)
    else:
        user = db.get_all_info(current_user_id)
        bot.send_message(message.chat.id, f"*User Info:*\n\n{user}", parse_mode='Markdown', reply_markup=keyboard)


def get_payment_info(bot, db, message):
    global payment_id
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Back', callback_data='admin')
    keyboard.add(back_button, row_width=1)
    payment_id = message.text
    if not db.payment_exist(payment_id):
        bot.send_message(message.chat.id, "*Payment Not Found*", parse_mode='Markdown', reply_markup=keyboard)
    else:
        payment = db.get_payment_info(payment_id)
        bot.send_message(message.chat.id, f"*Payment Info:\n\n{payment}*", parse_mode='Markdown', reply_markup=keyboard)
