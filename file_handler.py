import json
import os

class JSONFileHandler:
    @staticmethod
    def read(path) -> list:
        if '.json' in path:
            with open(path, 'r') as file:
                config = json.load(file)
            return config
        else:
            file_name, file_extension = os.path.splitext(path)
            raise ValueError(f"Expected JSON, but received an {file_extension}")
    @staticmethod
    def write(data, path):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
