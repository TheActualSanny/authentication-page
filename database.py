import psycopg2
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

class db_manager:
    def connector(self):
        self._conn = psycopg2.connect(
            host = config['POSTGRES_DATA']['HOST'],
            user = config['POSTGRES_DATA']['USER'],
            password = config['POSTGRES_DATA']['PASS'],
            database = config['POSTGRES_DATA']['DB']
        )
        self._cur = self._conn.cursor()
        self._cur.execute('''CREATE TABLE IF NOT EXISTS user_data(
                          id SERIAL PRIMARY KEY,
                          username text,
                          password text
        )''')
    def disconnect(self):
        self._conn.close()
        self._cur.close()

    def insert_data(self, username, password):
        self.connector()
        with self._conn:
            self._cur.execute('INSERT INTO user_data(username, password) VALUES(%s, %s)', (username, password))
        self.disconnect()
    
    def checker(self, username):
        self.connector()
        self._cur.execute('SELECT * FROM user_data WHERE username = %s', (username, ))
        if self._cur.fetchall():
            return True
        self.disconnect()
