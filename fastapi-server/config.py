import json


# Returns the value corresponding to the input key from the config.json file:
def read_config(key: str):
    # 'r' means read-only:
    with open("config.json", "r") as file:
        return json.load(file).get(key)