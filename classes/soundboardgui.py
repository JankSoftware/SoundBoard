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
    root.attributes('-toolwindow', True)
    root.resizable(False, False) 
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
        self.__AddButtonsFromSounds()
        self.__CreateMenuBar()
   
    def __CreateMenuBar(self):        
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.removeMenu =  Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="New", command= lambda: self.__createButton())
        self.filemenu.add_cascade(label="Remove", menu=self.removeMenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)        
       
        for s in self.sc.GetSounds():
            self.removeMenu.add_command(label=f"{s.id} - {s.name}", command= lambda: self.__removeSound(s.id))
        
        # TODO: Add about menu
        # helpmenu = Menu(menubar, tearoff=0)
        # helpmenu.add_command(label="About...")
        # menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=self.menubar)
        self.root.mainloop()

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

    def __RefreshButtons(self):
        self.frame.destroy()
        self.frame = Frame(self.root)
        self.frame.grid()
        self.sc.LoadSounds(self.db.SelectAll())
        self.__AddButtonsFromSounds()
        
    def __RefreshRemoveMenu(self):  
        self.removeMenu.delete(0, END)
        for s in self.sc.GetSounds():
            self.removeMenu.add_command(label=f"{s.id} - {s.name}", command=lambda: self.__removeSound(s.id))

    def __buttonClick(self, id):
        self.sc.PlaySoundById(id)

    def __AddButtonsFromSounds(self):
        col = 0
        row = 0
        sound_list = self.sc.GetSounds()
        if len(sound_list) > 0:
            for s in sound_list:
                self.__initialize_button(col, row, s)
                if row >= self.max_row - 1:
                    row = 0
                    col += 1
                    if col > self.max_column - 1:
                        break
                else:
                    row +=1
        else:
            self.buttons[-1] = Button(
                self.frame, 
                text="None", 
                bg="gray", 
                fg="white", 
                font="Impact", 
                height=self.button_height, 
                width=self.button_width).grid(
                    row=0, 
                    column=0)

    def __removeSound(self, id):
        self.db.Delete(id)
        self.__RefreshButtons()
        self.__RefreshRemoveMenu()

    def __createButton(self):
        new_sound_name = tkinter.simpledialog.askstring("New Button", "Enter a name: ")
        if new_sound_name != None:
            currdir = SoundboardConfig.sound_files_path
            file = tkinter.filedialog.askopenfilename(parent=self.root, initialdir=currdir, title='Please select a directory')
            self.db.Insert(new_sound_name, file)
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.__RefreshButtons()
            self.__RefreshRemoveMenu()

    def Run(self):
        self.root.mainloop()