attributes = ["user_id", "first_name", "last_name", "user_type", "phone", "comment", "status", "start_at", "end_at",
              "create_by", "create_at", "update_by", "update_at"]
create_table = "CREATE TABLE purchases (\n" \
               "    purchase_id SERIAL PRIMARY KEY,\n" \
               "    telegram_id INTEGER NOT NULL,\n" \
               "    total_amount INTEGER NOT NULL,\n" \
               "    status BOOLEAN NOT NULL,\n" \
               "    purchase_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n" \
               ");"
drop_table = "DROP TABLE purchases"
insert_query = "INSERT INTO purchases (telegram_id, total_amount, status) VALUES ({!r}, {!r}, {!r})"
update_query = "UPDATE purchases SET telegram_id={!r}, total_amount={!r}  status={!r} WHERE purchase_id={!r}"
delete_query = "DELETE FROM purchases WHERE purchase_id={!r}"


def inset_purchase(database, telegram_id, total_amount, status):
    return database.execute(insert_query.format(telegram_id, total_amount, status))


def update_purchase(database, client_id, key, value):
    return database.execute(update_query.format(client_id, key, value))


def delete_purchase(database, client_id):
    return database.execute(delete_query.format(client_id))
