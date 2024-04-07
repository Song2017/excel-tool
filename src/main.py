from src.db.db_query import execute_query

import json


def loader() -> dict:
    with open("./src/data/conf.json") as f:
        conf = json.loads(f.read())
    return conf


def main():
    conf = loader()
    for k, v in conf.items():
        # sheet
        ...
    import pdb;
    pdb.set_trace()
    rows = execute_query("", {})


if __name__ == '__main__':
    main()
