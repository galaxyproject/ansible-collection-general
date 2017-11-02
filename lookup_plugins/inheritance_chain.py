from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
"""

EXAMPLES = """
"""

RETURN = """
"""


from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        try:
            assert 'group_names' in variables, "Missing 'group_names' in variables"
            assert len(terms) == 1, "Inheritance chain lookup plugin expects 1 term, got %s" % len(terms)
        except AssertionError as exc:
            raise AnsibleError(str(exc))
        _vars = variables or {}
        base = terms[0]
        r = []
        for prefix in ['all', 'group'] + [n + '_group' for n in _vars['group_names']] + ['host']:
            _var = prefix + '_' + base
            _val = _vars.get(_var, [])
            if _val:
                display.vvvv('%s = %s' % (_var, _val))
            try:
                t = self._templar.template(
                    _vars.get(_var, []), preserve_trailing_newlines=True,
                    convert_data=True, escape_backslashes=False)
            except Exception as exc:
                raise AnsibleError("Templating '%s' failed: %s" % (_var, str(exc)))
            if t != _val:
                display.vvvv('%s -> %s' % (_var, t))
            r.extend(t)
        # this is actually not invalid if the name is valid, and there's no way
        # to default in the playbook, so we'll just return an empty list here
        #if not r:
        #    raise AnsibleError("No inheritance chain variables exist for base '%s'" % base)
        return r
