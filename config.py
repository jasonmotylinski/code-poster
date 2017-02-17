import yaml

_Config = None


def get():
    global _Config
    if _Config is None:
        _Config = yaml.load(open('config.yml', 'r'))

    return _Config
