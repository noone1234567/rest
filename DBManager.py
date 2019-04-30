import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('news.db', check_same_thread=False)

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class NewsModel:
    def __init__(self, conn):
        self.conn = conn

        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 title VARCHAR(100),
                                 content VARCHAR(1000),
                                 user_id INTEGER
                                 )''')
        cursor.close()
        self.conn.commit()

    def insert(self, title, content, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (title, content, str(user_id)))
        cursor.close()
        self.conn.commit()

    def get(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, news_id=None):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title FROM news")

        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.conn.commit()

    def update(self, news_id, part, text):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE news SET {} = '{}' WHERE id = {}".format(part, text, str(news_id)))
        cursor.close()
        self.conn.commit()


class UserModel(DB):
    def init(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 user_name VARCHAR(50),
                                 password_hash VARCHAR(128)
                                 )''')
        if not self.exists('duny', '1234567')[0]:
            cursor.execute('''INSERT INTO users 
                                             (user_name, password_hash) 
                                             VALUES (?,?)''', ('duny', '1234567'))
            cursor.execute('''INSERT INTO users 
                                                     (user_name, password_hash) 
                                                     VALUES (?,?)''', ('avengers', '1234567'))

        cursor.close()
        self.conn.commit()

    def exists(self, user_name, password_hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False, self.count_users()[0] + 1)

    def get(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def count_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM users")
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_name FROM users")
        rows = cursor.fetchall()
        return rows

    def insert(self, user_name, password_hash):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users 
                             (user_name, password_hash) 
                             VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.conn.commit()

