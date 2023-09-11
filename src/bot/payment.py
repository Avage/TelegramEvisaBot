from telebot import types
from src.utils import var_extractor
from src.utils.var_extractor import get_messages_var as msg
from src.crypto import payment


def send_payment_type(bot, db, call):
    if db.update_user_info_with_atr(call.from_user, "last_command", "payment_type"):
        keyboard = types.InlineKeyboardMarkup()
        card_button = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'card_button'),
                                                 callback_data='card')
        crypto_button = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'crypto_button'),
                                                   callback_data='crypto')
        cancel_button = types.InlineKeyboardButton(msg(db.get_lg(call.from_user), 'cancel_button'),
                                                   callback_data='start')
        keyboard.add(card_button, crypto_button, cancel_button, row_width=1)
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'payment_type_message'),
                         reply_markup=keyboard, parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')


def send_card_payment(bot, db, call):
    code = str(db.get_user_info_with_atr(call.from_user, "visa_code"))
    item = next(
        (dic for dic in var_extractor.get_config_var("single" if code[0] == "1" else "multiple") if
         dic['code'] == code), None)
    bot.send_invoice(call.message.chat.id, title=item["title"], description=item["description"],
                     invoice_payload=item["code"],
                     provider_token=var_extractor.get_env_var("STRIPE_INVOICE_TOKEN"),
                     currency=item["currency"],
                     prices=[types.LabeledPrice(item["title"], item["price"] * 100)])


def send_crypto_payment(bot, db, call):
    code = str(db.get_user_info_with_atr(call.from_user, "visa_code"))
    item = next(
        (dic for dic in var_extractor.get_config_var("single" if code[0] == "1" else "multiple") if
         dic['code'] == code), None)
    resp = payment.get_pay_link(item["currency"], item["price"], call.message.chat.id)
    if resp.startswith("Error"):
        bot.send_message(var_extractor.get_env_var("ADMIN_ID"), resp)
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'went_wrong_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, msg(db.get_lg(call.from_user), 'crypto_link_message') + f"\n\n{resp}",
                         parse_mode='Markdown')


def successful_card_payment(bot, db, message):
    if db.add_card_payment(message.content_type, message.from_user, message.successful_payment):
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'success_payment_message'),
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg(db.get_lg(message.from_user), 'payment_error_message'),
                         parse_mode='Markdown')
        bot.send_message(var_extractor.get_env_var("ADMIN_ID"),
                         f"Error: Can't add card to database.\n\nUser: {message.from_user}")


def successful_crypto_payment(bot, db, call):
    if db.add_crypto_payment(call.data, call.from_user, call.message.successful_payment):
        bot.send_message(call.chat.id, msg(db.get_lg(call.from_user), 'success_payment_message'), parse_mode='Markdown')
    else:
        bot.send_message(call.chat.id, msg(db.get_lg(call.from_user), 'payment_error_message'), parse_mode='Markdown')
        bot.send_message(var_extractor.get_env_var("ADMIN_ID"),
                         f"Error: Can't add crypto to database.\n\nUser: {call.from_user}")
