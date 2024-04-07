import json


def loader() -> dict:
    with open("./src/data/conf.json") as f:
        conf = json.loads(f.read())
    return conf

