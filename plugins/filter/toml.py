import toml
import json


def to_toml(v):
    s = json.dumps(dict(v))
    d = json.loads(s)
    return toml.dumps(d)


class FilterModule(object):
    def filters(self):
        return {
            'to_toml': to_toml,
        }
