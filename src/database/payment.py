from datetime import datetime, timezone


def add_card_payment(conn, content, user, payment):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO payments (id, user_id, paid, send_to_admin, passport, visa_type, payment, price, currency,"
            " date_time)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (payment.provider_payment_charge_id, user.id, True if content == "successful_payment" else False,
             False, None, payment.invoice_payload, "card", payment.total_amount / 100, payment.currency,
             datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")))
        conn.commit()
        return True
    except Exception as err:
        print('Cause: {}'.format(err))
        return False


def add_crypto_payment(conn, payload):
    try:
        c = conn.cursor()
        conn.commit()
        return True
    except Exception as err:
        print('Cause: {}'.format(err))
        return False
