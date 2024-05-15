from methods import user
from methods import purchase
from methods import tariff
from models import shared, DataBase
from utils import const

tables = [user, purchase, tariff]


async def init_database(connection_db):
    msg = []
    for table in tables:
        msg.append(str(connection_db.execute(table.create_table)['msg']))
    return msg


async def delete_database(connection_db):
    msg = []
    for table in tables:
        msg.append(str(connection_db.execute(table.drop_table)['msg']))

    return msg


async def initial(connection_db):
    s = await init_database(connection_db)
    print("".join(s))


async def uninstall(connection_db):
    s = await delete_database(connection_db)
    print("".join(s))


async def connection():
    print("Connect database...")
    con = DataBase().connect()
    shared.database = con


async def re_connection(client, msg, err):
    await msg.reply_text("Keyinroq urinib ko'ring ")
    await connection()
    await client.send_message(const.ADMINS[0], str(err))
