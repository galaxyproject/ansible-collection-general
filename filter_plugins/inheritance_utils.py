from collections import OrderedDict


def subelement_union(chain, key, subkey):
    # this will not merge any keys other than subkey, and subkey must be a list
    r = OrderedDict()
    # if a lookup plugin is called in the variable context and returns a
    # one-element list, the return value is replaced with the element
    chain = [chain] if not isinstance(chain, list) else chain
    for d in chain:
        if d[key] in r:
            r[d[key]][subkey].extend(filter(lambda i: i not in r[d[key]][subkey], d[subkey]))
        else:
            r[d[key]] = d
    return list(r.values())


class FilterModule(object):
    def filters(self):
        return {
            'subelement_union': subelement_union,
        }
