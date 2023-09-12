from datetime import datetime, timezone


def add_payment(conn, user, payment_type, price, currency):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO payments (visa_code, passport_name, passport_surname, "
                  "passport_number, passport_birthday, passport_photo, passport_scan, passport_photo_msg_id, "
                  "passport_scan_msg_id, msg_id) SELECT visa_code, passport_name, passport_surname, "
                  "passport_number, passport_birthday, passport_photo, passport_scan, passport_photo_msg_id, "
                  f"passport_scan_msg_id, msg_id FROM users WHERE id = {user.id} RETURNING id")
        last_row_id = c.fetchone()[0]
        time = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M:%S')
        c.execute(
            f"UPDATE payments SET user_id={user.id}, paid={False}, send_to_admin={False}, payment='{payment_type}', "
            f"price={price}, currency='{currency}', date_time='{time}' WHERE id = {last_row_id}")
        conn.commit()
        return last_row_id
    except Exception as err:
        print('Cause: {}'.format(err))
        return False


def make_paid(conn, row_id, tg_invoice_id, service_invoice_id):
    try:
        c = conn.cursor()
        c.execute(f"UPDATE payments SET paid={True}, send_to_admin={False}, telegram_invoice_id='{tg_invoice_id}', "
                  f"service_invoice_id='{service_invoice_id}' WHERE id = {row_id}")
        conn.commit()
        return True
    except Exception as err:
        print('Cause: {}'.format(err))
        return False

# def add_card_payment(conn, content, user, payment):
#     try:
#         c = conn.cursor()
#         c.execute(
#             "INSERT INTO payments (id, user_id, paid, send_to_admin, passport, visa_type, payment, price, currency,"
#             " date_time)"
#             "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#             (payment.provider_payment_charge_id, user.id, True if content == "successful_payment" else False,
#              False, None, payment.invoice_payload, "card", payment.total_amount / 100, payment.currency,
#              datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")))
#         conn.commit()
#         return True
#     except Exception as err:
#         print('Cause: {}'.format(err))
#         return False
#
#
# def add_crypto_payment(conn, payload):
#     try:
#         c = conn.cursor()
#         conn.commit()
#         return True
#     except Exception as err:
#         print('Cause: {}'.format(err))
#         return False
