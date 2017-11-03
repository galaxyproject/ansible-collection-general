from collections import OrderedDict
from functools import partial
from itertools import chain

from ansible.errors import AnsibleError


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


def _try_keys(i, kk, vk):
    try:
        if isinstance(i, list):
            # will raise IndexError if it's missing an element
            return (i[0], i[1])
        if isinstance(i, dict) and len(i) != 1:
            # will raise KeyError if either key doesn't exist
            return (i[kk], i[vk])
        if isinstance(i, dict):
            return (i.keys()[0], i.values()[0])
        else:
            raise TypeError()
    except Exception as exc:
        raise exc.__class__(i, exc)


def _islist(i):
    assert isinstance(i, list) or isinstance(i, tuple), i


def ordered(*iterables, **kwargs):
    """Merge iterables into an ordered dictionary and return them as a list of pairs

    Useful for merging lists of defaults that you want to keep in order

    Does not merge recursively (but that could be added from the built-in
    combine filter if necessary).

    Does not return an OrderedDict directly because Ansible doesn't support the
    data type and converts it in to its string representation.

    Elements of iterables are themselves an iterable, whose items can be:
      - two-item lists, where i[0] is the key and i[1] is the value
      - one-item dicts where the key is the key and the value is the value
      - dicts where i[k_key] is the key and i[v_key] is the value
    """
    k_key = kwargs.get('k_key', 'key')
    v_key = kwargs.get('v_key', 'value')
    try_keys = partial(_try_keys, kk=k_key, vk=v_key)
    try:
        _islist(iterables)
        map(_islist, iterables)
    except AssertionError as exc:
        raise AnsibleError("|ordered expects lists, got " + repr(exc[0]))
    try:
        return list(OrderedDict(map(try_keys, chain(*iterables))).items())
    except IndexError as exc:
        raise AnsibleError("|ordered must have 2 list elements %s: %s" % (exc[0], repr(exc[1])))
    except KeyError as exc:
        raise AnsibleError("|ordered key not found in dict (hash) list element %s: %s" % (exc[0], repr(exc[1])))
    except TypeError as exc:
        raise AnsibleError("|ordered list element must be list or dict, got " + repr(exc[0]))


class FilterModule(object):
    def filters(self):
        return {
            'subelement_union': subelement_union,
            'ordered': ordered,
        }
