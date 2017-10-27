from collections import OrderedDict


def subelement_union(chain, key, subkey):
    # this will not merge any keys other than subkey, and subkey must be a list
    r = OrderedDict()
    for d in chain:
        if d[key] in r:
            r[d[key]][subkey].extend(filter(lambda i: i not in r[d[key]][subkey], d[subkey]))
        else:
            r[d[key]] = d
    return list(r.values())


def chain_vars(base, _vars):
    r = []
    gprefixes = [n + '_group' for n in _vars['group_names']]
    for prefix in ['all', 'group'] + gprefixes + ['host']:
        r.extend(_vars.get(prefix + '_' + base, []))
    return r


class FilterModule(object):
    def filters(self):
        return {
            'subelement_union': subelement_union,
            'chain_vars': chain_vars,
        }
