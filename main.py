from src.bot import bot
from src.utils import var_extractor
from src.server import sv
from src.database import db


def main():
    try:
        user_db = db.db()
        bot_token = var_extractor.get_env_var('BOT_TOKEN')
        tg_bot = bot.Bot(bot_token, user_db)
        sv.create_app(tg_bot.bot)

    except Exception as err:
        print('Cause: {}'.format(err))


if __name__ == '__main__':
    main()
