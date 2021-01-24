from tkinter import *
import tkinter.simpledialog
import tkinter.filedialog
from classes.soundcontroller import SoundController
from classes.config import SoundboardConfig
from classes.dbcontroller import DBController

class GUI(object):

    #Creates window. Frame helps for refresh.
    root = Tk()
    root.title('Soundboard')
    root.iconbitmap = None
    frame = Frame(root)
    
    # Button constants
    button_width = 10
    button_height = 2
    max_column = 3
    max_row = 2

    buttons = {}

    def __init__(self, soundController: SoundController, dbController: DBController):
        self.db = dbController
        self.sc = soundController
        self.frame.grid()
        self.__LoadControlButtons()
        self.__AddButtonsFromSounds()

    def __LoadControlButtons(self):
        self.buttons[-2] =  Button(self.frame, text="Add", bg="green", fg="white", font="Impact", height=self.button_height, width=self.button_width, command= lambda: self.__createButton()).grid(row=0, column=0)
        self.buttons[-1] =  Button(self.frame, text="Remove", bg="red", fg="white", font="Impact", height=self.button_height, width=self.button_width, command=  lambda: self.__deleteButton()).grid(row=1, column=0)
        self.buttons[0] = Button(self.frame, text="Refresh", bg="blue", fg="white", font="Impact", height=self.button_height, width=self.button_width).grid(row=2, column=0)

    def __initialize_button(self, column, row, sound):
        self.buttons[sound.id] = Button(
            self.frame, 
            text=sound.name, 
            bg="black", 
            fg="white", 
            font="Impact", 
            height=self.button_height, 
            width=self.button_width,
            command = lambda: self.__buttonClick(sound.id)).grid(
                row=row, 
                column=column)

    def __buttonClick(self, id):
        self.sc.PlaySoundById(id)

    def __AddButtonsFromSounds(self):
        # starting column is 1 since controls are on 0
        col = 1
        row = 0
        for s in self.sc.GetSounds():
            self.__initialize_button(col, row, s)
            if row >= self.max_row - 1:
                row = 0
                col += 1
                if col >= self.max_column + 1:
                    break
            else:
                row +=1

    def __deleteButton(self):
        master = Tk()
        listbox = Listbox(master)
        listbox.grid()

        local_list = {}

        for s in self.sc.GetSounds():
            local_list[f"{s.id} - {s.name}"] = s.id 
            listbox.insert(END, f"{s.id} - {s.name}")

        remove = Button(master, text="Remove", command=lambda: self.__removeSound(local_list[listbox.get(listbox.curselection())], master))
        remove.grid()
        mainloop()
        
    def __removeSound(self, id, master):
        self.db.Delete(id)
        master.destroy()

    def __createButton(self):
        new_sound_name = tkinter.simpledialog.askstring("New Button", "Enter a name: ")
        if new_sound_name != None:
            currdir = SoundboardConfig.sound_files_path
            file = tkinter.filedialog.askopenfilename(parent=self.root, initialdir=currdir, title='Please select a directory')
            self.db.Insert(new_sound_name, file)
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.__LoadControlButtons()
            self.__AddButtonsFromSounds()

    def Run(self):
        self.root.mainloop()