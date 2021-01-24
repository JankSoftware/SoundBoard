import sqlite3
from sqlite3 import Error
from classes.sound import Sound

class DBController(object):

    def __init__(self, path):
         self.dbpath = path
         self.__create_connection()
         self.__check_db_exists()

    def __create_connection(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.dbpath)
            print("Connection to SQLite DB successful!")
        except Error as e:
            print(f"The error '{e}' occurred.")

    def __close_connection(self):
        try:
            self.connection.close()
            print("Connection to SQLite DB closed!")
        except Error as e:
            print(f"The error '{e}' occurred.")

    def __check_db_exists(self):
        if self.connection != None:
            db = self.connection.cursor()
            row = db.execute('SELECT name FROM sqlite_master WHERE type =\'table\' AND name =\'sounds\';').fetchall()
            if len(row) <= 0:
                self.__create_database()
                print("New DB created")
            else:
                print("DB alreadey exists")          

    def __create_database(self):
        db = self.connection.cursor()
        try:
            db.execute('CREATE TABLE IF NOT EXISTS sounds (id INTEGER PRIMARY KEY, name_text NOT NULL, path_text NOT NULL)')
            print("Create DB successful!")
        except Error as e:
            print(f"The error '{e}' occurred.")

    def __clear_database(self):
        db = self.connection.cursor()
        db.execute('''DROP TABLE sounds''')

    def Insert(self, name, path):
        db = self.connection.cursor()
        try:
            db.execute(f"INSERT INTO sounds (name_text, path_text) VALUES ('{name}', '{path}');")
            self.connection.commit()
            print(f"Added sound '{name}'' at '{path}'")
        except Error as e:
            print(f"The error '{e}' occurred.")

    def Delete(self, id):
        db = self.connection.cursor()
        try:
            db.execute(f"DELETE FROM sounds WHERE id == '{id}';")
            self.connection.commit()
            print(f"Deleted sound id {id}")
        except Error as e:
            print(f"The error '{e}' occurred.")

    def SelectAll(self, alphabetical=True):
        db = self.connection.cursor()
        query = lambda alpha: 'SELECT * FROM sounds ORDER BY name_text;' if alpha == True else 'SELECT * FROM sounds;' 
        print(query(alphabetical))
        results = []
        for row in db.execute(query(alphabetical)):
            print(row)
            results.append((row[0], row[1], row [2]))
        return results
