import json


class JSONContextManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def __enter__(self):
        # Read the JSON file
        with open(self.filename, "r") as file:
            self.data = json.load(file)
        return self.data

    def __exit__(self, exc_type, exc_value, traceback):
        # Write the modified JSON data back to the file
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

        # Propagate any exceptions
        return False
