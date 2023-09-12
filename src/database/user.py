def add_user(conn, user):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (id, username, firstname, language, last_command, visa_code, passport_name, "
            "passport_surname, passport_number, passport_birthday, passport_photo, passport_scan, "
            "passport_photo_msg_id, passport_scan_msg_id, msg_id)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user.id, None, None, user.language_code, "start", None, None, None, None, None, None,
             None, None, None, None))
        conn.commit()
        c.execute(f"UPDATE users SET username = ('%s') WHERE id = {user.id}" % user.username)
        c.execute(f"UPDATE users SET firstname = ('%s') WHERE id = {user.id}" % user.first_name)
        conn.commit()
        return True
    except Exception as err:
        print('Cause: {}'.format(err))
        return False


def user_exist(conn, user):
    try:
        c = conn.cursor()
        c.execute(f"SELECT id FROM users WHERE id = {user.id}")
        if c.fetchone():
            return True
        else:
            return False
    except Exception as err:
        print('Cause: {}'.format(err))
        return False


def get_lg(conn, user):
    try:
        c = conn.cursor()
        c.execute(f"SELECT language FROM users where id = {user.id}")
        return c.fetchone()[0]
    except Exception as err:
        print('Cause: {}'.format(err))
        return 'en'


def get_user_info_with_atr(conn, user, atr):
    try:
        c = conn.cursor()
        c.execute(f"SELECT (%s) FROM users where id = {user.id}" % atr)
        return c.fetchone()[0]
    except Exception as err:
        print('Cause: {}'.format(err))
        return None


def update_user_info_with_atr(conn, user, atr, new_value):
    try:
        c = conn.cursor()
        c.execute(f"UPDATE users SET {atr} = ('%s') WHERE id = {user.id}" % new_value)
        conn.commit()
        return True
    except Exception as err:
        print('Cause: {}'.format(err))
        return False
