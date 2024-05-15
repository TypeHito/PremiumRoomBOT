from models import User


create_table = "CREATE TABLE users (\n" \
               "    user_id SERIAL PRIMARY KEY,\n" \
               "    telegram_id BIGINT UNIQUE NOT NULL,\n" \
               "    first_name VARCHAR(50) NOT NULL,\n" \
               "    enter_name VARCHAR(50),\n" \
               "    user_name VARCHAR(50),\n" \
               "    is_premium BOOLEAN,\n" \
               "    phone VARCHAR(20),\n" \
               "    total_amount BIGINT,\n" \
               "    purchase_count INTEGER,\n" \
               "    rate INTEGER,\n" \
               "    review VARCHAR(255),\n" \
               "    referral_id BIGINT,\n" \
               "    referrals_count INTEGER,\n" \
               "    bot_menu VARCHAR(50),\n" \
               "    update_by BIGINT,\n" \
               "    init_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n" \
               "    start_at TIMESTAMP,\n" \
               "    end_at TIMESTAMP\n," \
               "    premium_status BOOLEAN\n" \
               ");"
drop_table = "DROP TABLE users"
insert_query = "INSERT INTO users (telegram_id, first_name, is_premium) VALUES ({!r}, {!r}, {!r});"
update_bot_menu_query = "UPDATE users  SET bot_menu={!r} WHERE telegram_id={!r};"
update_contact_query = "UPDATE users  SET phone={!r} WHERE telegram_id={!r};"
update_subscription_query = ("UPDATE users "
                             "SET update_by = {!r}, start_at = '{}', end_at = '{}', premium_status = True "
                             "WHERE telegram_id={!r};")
update_subscription_end_query = ("UPDATE users "
                                 "SET premium_status = False, update_by = {!r}, end_at = '{}'"
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


async def inset_user(database, telegram_id, first_name, is_premium):
    database.execute(insert_query.format(telegram_id, first_name, is_premium))


async def update_bot_menu(database, client_id, value):
    database.execute(update_bot_menu_query.format(value, client_id))


async def update_contact(database, client_id, value):
    database.execute(update_contact_query.format(value, client_id))


async def update_subscription(database, client_id, update_by, start_at, end_at):
    database.execute(update_subscription_query.format(update_by, start_at, end_at, client_id))


async def update_subscription_end(database, client_id, update_by, end_at):
    database.execute(update_subscription_end_query.format(update_by,  end_at, client_id))


async def delete_client(database, client_id):
    database.select(delete_query.format(client_id))


async def get_user(database, client_id) -> User:
    user = database.select_one(select_telegram_id_query.format(client_id))
    return User(*user)

