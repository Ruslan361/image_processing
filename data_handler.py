import file_handler
import os

class DataHandler:
    def __init__(self, filename='config.json'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(dir_path, filename)

    def load(self, group):
        return file_handler.JSONFileHandler.read(self.path)[group]
    def write(self, group, data):
        if os.path.exists(self.path):
            settingsInFile = file_handler.JSONFileHandler.read(self.path)
            settingsInFile[group] = data
        else:
            settingsInFile = {group: data}
        file_handler.JSONFileHandler.write(settingsInFile, self.path)