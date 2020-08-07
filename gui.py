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

#Creates window. Frame helps for refresh.
root = Tk()
frame = Frame(root)

#Iterator to help with button row stuff
x = 0

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

def initialize_buttons(row, index):
    name = row[0]
    newButton = Button(frame, text=name, bg="black", fg="white", font="Impact", height=5, width=25, command = lambda: buttonClick(name))
    newButton.grid(row=index, column=1)

def createButton():
    answer = tkinter.simpledialog.askstring("New button", "Enter a name: ")
    currdir = os.getcwd()
    file = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    newButton = Button(frame, text=answer, bg="black", fg="white", font="Impact", height=5, width=25, command = lambda: buttonClick(answer))
    newButton.grid()
    add_to_database(answer, file)
    read_database()

def deleteButton(text):
    index = text[0]
    conn = create_connection(database_path)
    db = conn.cursor()
    i = 0
    for row in db.execute('SELECT * FROM sounds ORDER BY name'):
        if i == index:
            sound_name = row[0]
        i = i+1
    db.execute(f"DELETE from sounds WHERE name = '{sound_name}'")
    conn.commit()
    conn.close()

def list_buttons():
    master = Tk()

    listbox = Listbox(master)
    listbox.grid()

    conn = create_connection(database_path)
    db = conn.cursor()
    for row in db.execute('SELECT * FROM sounds ORDER BY name'):
        listbox.insert(END, row[0])

    remove = Button(master, text="Remove", command=lambda: deleteButton(listbox.curselection()))
    remove.grid()

    mainloop()

#PLEASE FIX THIS IT DOESNT WORK RIGHT NOW
#MAKES AN EXTRA WOO CAUSE ROWS SHIFT AND EVERYTHING COVERS ITSELF
def refreshButton():
    i = 0
    for widget in frame.winfo_children():
        widget.destroy()
    #homeButtons()
    conn = create_connection(database_path)
    db = conn.cursor()
    for row in db.execute('SELECT * FROM sounds ORDER BY name'):
        initialize_buttons(row, i)
        i = i+1
    conn.commit()
    conn.close()
#Creates button widget
add = Button(frame, text="Add", bg="green", fg="white", font="Impact", height=5, width=25, command=createButton)
clear = Button(frame, text="Clear", bg="red", fg="white", font="Impact", height=5, width=25, command=clear_database)
remove = Button(frame, text="Remove", bg="orange", height=5, fg="white", font="Impact", width=25, command=list_buttons)
refresh = Button(frame, text="Refresh", bg="blue", fg="white", font="Impact", height=5, width=25, command=refreshButton)


#Inserts button widget
def homeButtons():
    add.grid(row=0, column=0)
    clear.grid(row=1, column=0)
    remove.grid(row=2, column=0)
    refresh.grid(row=3, column=0)

#Creates database and initial buttons
create_database()
conn = create_connection(database_path)
db = conn.cursor()
for row in db.execute('SELECT * FROM sounds ORDER BY name'):
    initialize_buttons(row, x)
    x = x+1

#Packs the frame
frame.grid()
homeButtons()
#Main loop
root.mainloop()
