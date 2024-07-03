from models import User
from utils import lang
from methods import timer
from utils import const

create_table = "CREATE TABLE users (\n" \
               "    user_id SERIAL PRIMARY KEY,\n" \
               "    telegram_id BIGINT UNIQUE NOT NULL,\n" \
               "    first_name VARCHAR(50) NOT NULL,\n" \
               "    enter_name VARCHAR(50),\n" \
               "    user_name VARCHAR(50),\n" \
               "    is_premium BOOLEAN,\n" \
               "    phone VARCHAR(20),\n" \
               "    total_amount BIGINT NOT NULL DEFAULT 0,\n" \
               "    purchase_count INTEGER NOT NULL DEFAULT 0,\n" \
               "    rate INTEGER,\n" \
               "    review VARCHAR(255),\n" \
               "    referral_id BIGINT,\n" \
               "    referrals_count INTEGER NOT NULL DEFAULT 0,\n" \
               "    bot_menu VARCHAR(50),\n" \
               "    update_by BIGINT,\n" \
               "    init_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n" \
               "    start_at TIMESTAMP,\n" \
               "    end_at TIMESTAMP,\n" \
               "    premium_status BOOLEAN,\n" \
               "    language VARCHAR(50)\n" \
               ");"
drop_table = "DROP TABLE users"
insert_query = ("INSERT INTO users (telegram_id, first_name, is_premium, referral_id, referrals_count) "
                "VALUES ({!r}, {!r}, {!r}, {!r}, 0);")
update_bot_menu_query = "UPDATE users  SET bot_menu={!r} WHERE telegram_id={!r};"
update_contact_query = "UPDATE users  SET phone={!r}, bot_menu='' WHERE telegram_id={!r};"
update_language_query = "UPDATE users  SET language={!r}, bot_menu='' WHERE telegram_id={!r};"
update_referral_query = "UPDATE users  SET referral_id={!r}, bot_menu='' WHERE telegram_id={!r};"
update_referral_count_query = "UPDATE users  SET referrals_count={!r} WHERE telegram_id={!r};"
update_subscription_query = ("UPDATE users "
                             "SET update_by = {!r}, start_at = '{}', end_at = '{}', premium_status = True "
                             "WHERE telegram_id={!r};")
update_subscription_end_query = ("UPDATE users "
                                 "SET premium_status = False, update_by = {!r}, end_at = '{}', bot_menu='' "
                                 "WHERE telegram_id={!r};")
update_premium_status_query = "UPDATE users SET {}={!r} WHERE telegram_id = {!r};"
delete_query = "DELETE FROM users WHERE telegram_id={!r};"
subscription_query = ("SELECT * FROM users "
                      "WHERE end_at < {!r} AND premium_status=True;")
select_all_query = "SELECT * FROM users;"
select_telegram_id_query = "SELECT * FROM users WHERE telegram_id = {!r} ;"


async def review_subscription(database, current_data: str):
    assert type(current_data) is str
    return database.select(subscription_query.format(current_data))


async def select_all(database):
    return database.select(select_all_query)


async def inset_user(database, msg, referrals=0):
    database.execute(insert_query.format(msg.from_user.id,
                              msg.from_user.first_name, msg.from_user.is_premium, referrals))


async def update_bot_menu(database, telegram_id, value):
    database.execute(update_bot_menu_query.format(value, telegram_id))


async def update_contact(database, telegram_id, value):
    database.execute(update_contact_query.format(value, telegram_id))


async def update_language(database, telegram_id, value):
    database.execute(update_language_query.format(value, telegram_id))


async def update_referral(database, telegram_id, value):
    database.execute(update_referral_query.format(value, telegram_id))


async def update_referral_count(database, referral: User):
    database.execute(update_referral_count_query.format(referral.referrals_count + 1, referral.telegram_id))


async def update_subscription(database, telegram_id, update_by, start_at, end_at):
    database.execute(update_subscription_query.format(update_by, start_at, end_at, telegram_id))


async def update_subscription_end(database, client_id, update_by, end_at=timer.get_current_time()):
    database.execute(update_subscription_end_query.format(update_by,  end_at, client_id))


async def delete_user(database, telegram_id):
    database.select(delete_query.format(telegram_id))


async def get_user(database, telegram_id) -> User:
    user = database.select_one(select_telegram_id_query.format(telegram_id))
    return User(*user)


def get_referral_id(referral_code) -> int:
    if str(referral_code).startswith("ref"):
        referral_id = referral_code[3:]
        return referral_id
    else:
        return 0


def get_current_language(user) -> {}:
    if user.language in lang.langs:
        return lang.langs[user.language]
    else:
        return {}

