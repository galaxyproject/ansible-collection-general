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
    def __chain_for_base(self, base, _vars):
        r = []
        if 'override_' + base in _vars:
            prefixes = ['override']
        else:
            prefixes = ['all', 'group', 'host']
            prefixes[2:2] = [n.replace('-', '_') + '_group' for n in _vars['group_names']]
        for prefix in prefixes:
            _var = prefix + '_' + base
            _val = _vars.get(_var, [])
            if _val:
                display.vvvv(f'{_var} = {_val}')
            try:
                t = self._templar.template(
                    _vars.get(_var, []), preserve_trailing_newlines=True,
                    convert_data=True, escape_backslashes=False)
            except Exception as exc:
                raise AnsibleError(f"Templating '{_var}' failed: {exc}")
            if t != _val:
                display.vvvv(f'{_var} -> {t}')
            r.extend(t)
        return r

    def run(self, terms, variables=None, **kwargs):
        try:
            assert 'group_names' in variables, "Missing 'group_names' in variables"
            assert len(terms) >= 1, f"Inheritance chain lookup plugin expects 1 or more terms, got {len(terms)}"
        except AssertionError as exc:
            raise AnsibleError(str(exc))
        _vars = variables or {}
        r = []
        for base in terms:
            r.extend(self.__chain_for_base(base, _vars))
        return r
