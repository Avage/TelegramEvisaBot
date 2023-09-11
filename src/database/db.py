import sqlite3
from src.database import user, payment


class db:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('bot_users', check_same_thread=False)
            c = self.conn.cursor()
            c.execute('''
                      CREATE TABLE IF NOT EXISTS users
                      ([id] INTEGER PRIMARY KEY, [username] TEXT, [firstname] TEXT, [language] TEXT, 
                      [last_command] TEXT, [visa_code] INTEGER, [passport_name] TEXT, [passport_surname] TEXT, 
                      [passport_number] TEXT, [passport_birthday], [passport_photo] TEXT, [passport_scan] TEXT, 
                      [passport_photo_msg_id] INTEGER, [passport_scan_msg_id] INTEGER)
                      ''')
            c.execute('''
                      CREATE TABLE IF NOT EXISTS payments
                        ([id] TEXT PRIMARY KEY, [user_id] INTEGER, [paid] INTEGER, [send_to_admin] INTEGER,
                         [passport] TEXT, [visa_type] TEXT, [payment] TEXT, [price] INTEGER, [currency] TEXT, 
                         [date_time] TEXT)
                        ''')
            self.conn.commit()
        except Exception as err:
            print('Cause: {}'.format(err))

    def add_user(self, usr):
        return user.add_user(self.conn, usr)

    def user_exist(self, usr):
        return user.user_exist(self.conn, usr)

    def get_lg(self, usr):
        return user.get_lg(self.conn, usr)

    def get_user_info_with_atr(self, usr, atr):
        return user.get_user_info_with_atr(self.conn, usr, atr)

    def update_user_info_with_atr(self, usr, atr, new_value):
        return user.update_user_info_with_atr(self.conn, usr, atr, new_value)

    def add_card_payment(self, content, usr, suc_payment):
        return payment.add_card_payment(self.conn, content, usr, suc_payment)

    def add_crypto_payment(self, payload):
        return payment.add_crypto_payment(self.conn, payload)
