from classes.dbcontroller import DBController
from classes.config import SoundboardConfig
from classes.soundcontroller import SoundController
from classes.soundboardgui import GUI

# Init database controller at the path set in the config
# which defaults to "this root dir\database\sounds.db"
db = DBController(SoundboardConfig.database_path)

# init sound controller
sc = SoundController()
sc.LoadSounds(db.SelectAll())

def main():
    gui = GUI(sc, db)
    gui.Run()

if __name__ == "__main__":
    main()