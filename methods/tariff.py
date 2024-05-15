"""Represents a currency with associated attributes, upholding safety and ethical principles."""
attributes = ["traffic_id", "title", "cost", "point", "status", "create_by", "create_at", "update_by", "update_at"]
create_table = "CREATE TABLE tariffs (\n" \
               "    tariff_id SERIAL PRIMARY KEY,\n" \
               "    title VARCHAR(100) NOT NULL UNIQUE,\n" \
               "    cost INTEGER,\n" \
               "    point INTEGER,\n" \
               "    status BOOLEAN\n" \
               ");"
drop_table = "DROP TABLE tariffs"
insert_query = "INSERT INTO tariffs (title, cost, point, status) VALUES ({!r}, {!r}, {!r}, {!r})"
update_query = "UPDATE tariffs  SET title={!r} cost={!r} point={!r} status={!r} WHERE tariff_id={!r}"
update_status_query = "UPDATE tariffs  SET title={!r} cost={!r} point={!r} status={!r} WHERE tariff_id={!r}"
delete_query = "DELETE FROM tariffs WHERE tariff_id={!r}"


def inset_traffic(database, title, cost, point, status):
    return database.execute(insert_query.format(title, cost, point, status))


def update_traffic(database, tariff_id, title, cost, point, status):
    return database.execute(update_query.format(title, cost, point, status, tariff_id))


def off_tariff(database, tariff_id, status):
    return database.execute(update_status_query.format(value, tariff_id))


def delete_traffic(database, client_id):
    return database.execute(delete_query.format(client_id))
