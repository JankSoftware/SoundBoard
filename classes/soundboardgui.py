from tkinter import *
import tkinter.simpledialog
import tkinter.filedialog
from classes.soundcontroller import SoundController

class GUI(object):

    #Creates window. Frame helps for refresh.
    root = Tk()
    root.title('Soundboard')
    root.iconbitmap = None
    frame = Frame(root)
    
    # Button constants
    button_width = 10
    button_height = 2
    max_column = 2
    max_row = 2

    buttons = {}

    def __init__(self, soundController: SoundController):
        self.sc = soundController
        self.frame.grid()
        self.__LoadControlButtons()
        self.__AddButtonsFromSounds()

    def __LoadControlButtons(self):
        self.buttons[-2] =  Button(self.frame, text="Add", bg="green", fg="white", font="Impact", height=self.button_height, width=self.button_width).grid(row=0, column=0)
        self.buttons[-1] =  Button(self.frame, text="Remove", bg="red", fg="white", font="Impact", height=self.button_height, width=self.button_width).grid(row=1, column=0)
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
            command = lambda: self.buttonClick(sound.id)).grid(
                row=row, 
                column=column)

    def buttonClick(self, id):
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

    def Run(self):
        self.root.mainloop()