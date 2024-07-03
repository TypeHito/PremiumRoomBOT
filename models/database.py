import psycopg2
from utils import const


class DataBase:
    host: str = const.db_host
    port: str = const.db_port
    database_name: str = const.db_database_name
    user: str = const.db_user
    password: str = const.db_password
    conn: psycopg2.connect = psycopg2.connect
    cur: psycopg2.connect = psycopg2.connect
    status: bool = False
    error: str = ""
    create_database: str = f"CREATE DATABASE {database_name}"
    delete_database: str = f"DELETE DATABASE {database_name}"

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database_name,
                user=self.user,
                password=self.password
            )
        except psycopg2.OperationalError as err:
            self.status = False
            self.error = err
        else:
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.status = True
        return self

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def execute(self, sql):
        error = ""
        try:
            self.cur.execute(sql)
        except (psycopg2.errors.DuplicateDatabase, psycopg2.errors.DuplicateTable,
                psycopg2.errors.UndefinedTable, psycopg2.errors.UniqueViolation,
                psycopg2.OperationalError,
                TypeError, AttributeError) as err:
            error = err
        else:
            self.conn.commit()
            return {'ok': True, 'msg': "Success!"}
        return {'ok': False, 'msg': error}

    def select(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_one(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()
