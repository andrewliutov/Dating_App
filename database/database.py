import sqlalchemy as sq
import psycopg2


class Database:
    def __init__(self, DSN):
        engine = sq.create_engine(DSN)
        self.mydb = engine.raw_connection()
        self.mycursor = self.mydb.cursor()

    def add_to_blacklist(self, id, liked):
        self.mycursor.execute(f'INSERT INTO users (vk_id, liked) VALUES({id}, {liked})')
        self.mydb.commit()

    def read_from_blacklist(self):
        self.mycursor.execute(
            f'CREATE TABLE IF NOT EXISTS users (vk_id integer NOT NULL default 0, liked boolean NOT NULL default False)')
        self.mydb.commit()
        self.mycursor.execute('SELECT vk_id FROM users')
        temp_list = self.mycursor.fetchall()
        blacklist = []
        for i in temp_list:
            blacklist.append(i[0])
        return blacklist
