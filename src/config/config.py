import pprint

from yaml import safe_load


def get_config(path):
    try:
        with open(path) as f:
            yml_dict = safe_load(f)

            print("Loaded config:")
            pprint.pp(yml_dict)

            return yml_dict
    except FileNotFoundError as e:
        print("No config found at path: " + path)
        return None
