#For the GUI
from tkinter import *
import tkinter.simpledialog

#For opening a file
import tkinter.filedialog
import os

#For the database
import sqlite3
from sqlite3 import Error

#Gets playsound files
from playsound import *

database_path = "c:\\users\\the goof troop\\desktop\\sound effects\\sounds.db"

root = Tk()

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to SQLite DB successful!")
    except Error as e:
        print(f"The error '{e}' occurred.")

    return connection

def create_database():
    conn = create_connection(database_path)
    db = conn.cursor()
    try:
        db.execute('''CREATE TABLE sounds
                  (name text, path text)''')
    except Error as e:
        print(f"The error '{e}' occurred.")

def clear_database():
    conn = create_connection(database_path)
    db = conn.cursor()
    db.execute('''DROP TABLE sounds''')

def add_to_database(name, path):
    conn = create_connection(database_path)
    db = conn.cursor()
    db.execute(f"INSERT INTO sounds VALUES ('{name}', '{path}')")
    conn.commit()
    conn.close()

def read_database():
    conn = create_connection(database_path)
    db = conn.cursor()
    for row in db.execute('SELECT * FROM sounds ORDER BY name'):
            print(row)
    conn.commit()
    conn.close()

def buttonClick(name):
    conn = create_connection(database_path)
    db = conn.cursor()
    for row in db.execute(f"SELECT * FROM sounds WHERE name='{name}'"):
        playsound(row[1])

def initialize_buttons(row):
    name = row[0]
    newButton = Button(root, text=name, padx=50, pady=50, command = lambda: buttonClick(name))
    newButton.pack()

def createButton():
    answer = tkinter.simpledialog.askstring("New button", "Enter a name: ")
    currdir = os.getcwd()
    file = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    newButton = Button(root, text=answer, padx=50, pady=50, command = lambda: buttonClick(answer))
    newButton.pack()
    add_to_database(answer, file)
    read_database()

#Creates button widget
add = Button(root, text="Add", padx=50, pady=50, command=createButton)
delete = Button(root, text="Delete", padx=50, pady=50, command=clear_database)


#Inserts button widget
add.pack()
delete.pack()
#Creates database and initial buttons
create_database()
conn = create_connection(database_path)
db = conn.cursor()
for row in db.execute('SELECT * FROM sounds ORDER BY name'):
    initialize_buttons(row)

#Main loop
root.mainloop()
