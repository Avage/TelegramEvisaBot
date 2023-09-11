from telebot import telebot, types
from src.database import db
from src.utils import var_extractor
from src.bot import settings, visas, details, payment
from src.utils.var_extractor import get_messages_var as msg


class Bot:
    def __init__(self, token, user_db):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.user_db: db.user = user_db

        self.set_webhook()

        @self.bot.message_handler(commands=['start', 'hello'])
        def set_menu(message):
            self.set_menu(message)

        @self.bot.message_handler(func=lambda msg: True)
        def get_message(message):
            self.get_message(message)

        @self.bot.message_handler(content_types=['photo'])
        def get_photo(message):
            self.get_photo(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            self.callback_query(call)

        @self.bot.pre_checkout_query_handler(func=lambda query: True)
        def pre_checkout_query(query):
            self.pre_checkout_query(query)

        @self.bot.message_handler(content_types=['successful_payment'])
        def successful_card_payment(message):
            payment.successful_card_payment(self.bot, self.user_db, message)

        @self.bot.message_handler(types=['ORDER_PAID'])
        def successful_card_payment(message):
            payment.successful_crypto_payment(self.bot, self.user_db, message)

    # Methods

    def set_webhook(self):
        self.bot.remove_webhook()
        self.bot.set_webhook(url=var_extractor.get_env_var("WEBHOOK_URL"))

    def set_menu(self, message):
        if not self.user_db.user_exist(message.chat):
            start_button = types.InlineKeyboardButton(msg('en', 'start_button'), callback_data='start')
            settings_button = types.InlineKeyboardButton(msg('en', 'settings_button'), callback_data='settings')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(start_button, settings_button, row_width=1)
            self.bot.send_message(message.chat.id, msg('en', 'welcome_message'), reply_markup=keyboard,
                                  parse_mode='Markdown')
            if not self.user_db.add_user(message.from_user):
                self.bot.send_message(message.chat.id, msg('en', 'went_wrong_message'), parse_mode='Markdown')
                self.send_error_to_admin(f"Error: Can't add user to database.\n\nUser: {message.chat.id}")
        else:
            start_button = types.InlineKeyboardButton(msg(self.user_db.get_lg(message.chat), 'start_button'),
                                                      callback_data='start')
            settings_button = types.InlineKeyboardButton(msg(self.user_db.get_lg(message.chat), 'settings_button'),
                                                         callback_data='settings')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(start_button, settings_button, row_width=1)
            self.bot.send_message(message.chat.id, msg(self.user_db.get_lg(message.chat), 'welcome_message'),
                                  reply_markup=keyboard,
                                  parse_mode='Markdown')

    def send_fail_message(self, call):
        self.bot.send_message(call.message.chat.id, msg(self.user_db.get_lg(call.from_user), 'went_wrong_message'),
                              parse_mode='Markdown')

    def send_error_to_admin(self, error):
        self.bot.send_message(var_extractor.get_env_var("ADMIN_ID"), error)

    def callback_query(self, call):
        data = call.data
        if data == "menu":
            self.set_menu(call.message)
        elif data == "settings":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "settings"):
                settings.send_settings(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "language":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "change_language"):
                settings.send_language_settings(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "en" or data == "ru":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "choose_language"):
                settings.change_language(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "start":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "start"):
                visas.send_visa_type(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "single" or data == "multiple":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "visa_type"):
                visas.send_visa_code(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif len(data) == 4 and data.isdigit():
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "visa_code"):
                details.get_name(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "confirm":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "confirm_details"):
                details.send_to_chat(self.bot, self.user_db, call)
                payment.send_payment_type(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "edit":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "visa_code"):
                details.get_name(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "card":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "card_payment"):
                payment.send_card_payment(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)
        elif data == "crypto":
            if self.user_db.update_user_info_with_atr(call.from_user, "last_command", "crypto_payment"):
                payment.send_crypto_payment(self.bot, self.user_db, call)
            else:
                self.send_fail_message(call)

    def get_message(self, message):
        atr = self.user_db.get_user_info_with_atr(message.from_user, "last_command")
        if atr == "get_name":
            details.get_last_name(self.bot, self.user_db, message)
        elif atr == "get_last_name":
            details.get_passport_number(self.bot, self.user_db, message)
        elif atr == "get_passport_number":
            details.get_passport_birthday(self.bot, self.user_db, message)
        elif atr == "get_passport_birthday":
            details.get_passport_photo(self.bot, self.user_db, message)
        elif atr == "get_passport_photo":
            self.bot.send_message(message.chat.id, msg(self.user_db.get_lg(message.chat), 'get_passport_photo_again'),
                                  parse_mode='Markdown')
        elif atr == "get_passport_scan":
            self.bot.send_message(message.chat.id, msg(self.user_db.get_lg(message.chat), 'get_passport_scan_again'),
                                  parse_mode='Markdown')
        else:
            self.bot.send_message(message.chat.id, msg(self.user_db.get_lg(message.chat), 'unrecognized_message'),
                                  parse_mode='Markdown')

    def get_photo(self, message):
        atr = self.user_db.get_user_info_with_atr(message.from_user, "last_command")
        if atr == "get_passport_photo":
            details.get_passport_scan(self.bot, self.user_db, message)
        elif atr == "get_passport_scan":
            details.confirm_details(self.bot, self.user_db, message)
        else:
            self.bot.send_message(message.chat.id, "*Sorry, something went wrong. Please try again later.*",
                                  parse_mode='Markdown')

    def pre_checkout_query(self, query):
        self.bot.answer_pre_checkout_query(query.id, ok=True)
