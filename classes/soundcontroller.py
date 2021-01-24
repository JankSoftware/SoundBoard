from classes.sound import Sound

class SoundController(object):

    def __init__(self):
        self._sounds = []

    def LoadSounds(self, sounds_to_load):
        for s in sounds_to_load:
            self._sounds.append(Sound(s[0], s[1], s[2]))
        print("Sounds loaded")

    def GetSounds(self):
        return self._sounds

    def GetSoundById(self, id):
        for s in self._sounds:
            if s.id == id:
                return s
        return None

    def GetSoundPathById(self, id):
        for s in self._sounds:
            if s.id == id:
                return s.path
        return None

    def GetSoundNameById(self, id):
        for s in self._sounds:
            if s.id == id:
                return s.name
        return None

    def PlaySoundById(self, id):
        for s in self._sounds:
            if s.id == id:
                s.play()
                break