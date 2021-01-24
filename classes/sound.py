from playsound import *

class Sound(object):

    def __init__(self, id, name, path):
        self.id = id
        self.name = name
        self.path = path

    def play(self):
        playsound(self.path)