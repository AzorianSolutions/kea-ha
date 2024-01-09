import re


class Config:
    """A class for interfacing with configuration data in object-like syntax with value variable parsing."""

    _root: any = None
    """The root context."""

    _context: any = {}
    """The current context."""

    _ref_pattern = re.compile(r'\$(c|e){([a-z_]+[a-z0-9_/]*)}', re.IGNORECASE)
    """ The regular expression pattern used to match variable references in values. """

    @property
    def root(self) -> any:
        """Returns the root context of the object."""
        return self._root

    @property
    def context(self) -> any:
        """Returns the context of the object."""
        return self._context

    def __init__(self, context: any, root: any = None):
        self._context = context
        self._root = root if root is not None else context

    def __call__(self, context: any):
        self._context = context

    def __lt__(self, other: any) -> bool:
        return self._context < other

    def __le__(self, other: any) -> bool:
        return self._context <= other

    def __eq__(self, other: any) -> bool:
        return self._context == other

    def __ne__(self, other: any) -> bool:
        return self._context != other

    def __gt__(self, other: any) -> bool:
        return self._context > other

    def __ge__(self, other: any) -> bool:
        return self._context >= other

    def __add__(self, other: any) -> any:
        return self._context + other

    def __sub__(self, other: any) -> any:
        return self._context - other

    def __getattr__(self, key: str) -> any:
        refs = key.split('.')
        ref = self._context
        for key in refs:
            try:
                ref = ref[key]
            except KeyError:
                raise AttributeError(f'Config context has no attribute "{key}"')
        return Config(ref, root=self._root)

    def __setattr__(self, key: str, value: any) -> None:
        try:
            if key in ['_context', '_root']:
                super().__setattr__(key, value)
                return
        except AttributeError:
            pass
        self._context[key] = value

    def __delattr__(self, key: str) -> None:
        del self._context[key]

    def __getitem__(self, key: str) -> any:
        return self._context[key]

    def __setitem__(self, key: str, value: any) -> None:
        getattr(self, key)(value)

    def __delitem__(self, key: str) -> None:
        del self._context[key]

    def __contains__(self, key: str) -> bool:
        return key in self._context

    def __iter__(self):
        return iter(self._context)

    def __len__(self):
        return len(self._context)

    def __repr__(self):
        return self.yaml()

    def __str__(self):
        if isinstance(self._context, dict) or isinstance(self._context, list):
            return self.yaml(self.parse(self._root, self._context))
        return str(self.parse(self._root, self._context))

    def __bool__(self):
        return bool(self._context)

    def __int__(self):
        return int(self._context)

    def __float__(self):
        return float(self._context)

    def __complex__(self) -> any:
        return complex(self._context)

    def __bytes__(self):
        return bytes(self._context)

    def __hash__(self):
        return hash(self._context)

    def __dir__(self):
        return dir(self._context)

    def __sizeof__(self):
        return self._context.__sizeof__()

    def __format__(self, format_spec: str):
        return self._context.__format__(format_spec)

    def __mul__(self, other: any) -> any:
        return self._context * other

    def __truediv__(self, other: any) -> any:
        return self._context / other

    def __floordiv__(self, other: any) -> any:
        return self._context // other

    def __mod__(self, other: any) -> any:
        return self._context % other

    def __divmod__(self, other: any) -> any:
        return divmod(self._context, other)

    def __pow__(self, other: any) -> any:
        return self._context ** other

    def __lshift__(self, other: any) -> any:
        return self._context << other

    def __rshift__(self, other: any) -> any:
        return self._context >> other

    def __and__(self, other: any) -> any:
        return self._context & other

    def __xor__(self, other: any) -> any:
        return self._context ^ other

    def __or__(self, other: any) -> any:
        return self._context | other

    def __radd__(self, other: any) -> any:
        return other + self._context

    def __rsub__(self, other: any) -> any:
        return other - self._context

    def __rmul__(self, other: any) -> any:
        return other * self._context

    def __rtruediv__(self, other: any) -> any:
        return other / self._context

    def __rfloordiv__(self, other: any) -> any:
        return other // self._context

    def __rmod__(self, other: any) -> any:
        return other % self._context

    def __rdivmod__(self, other: any) -> any:
        return divmod(other, self._context)

    def __rpow__(self, other: any) -> any:
        return other ** self._context

    def __rlshift__(self, other: any) -> any:
        return other << self._context

    def __rrshift__(self, other: any) -> any:
        return other >> self._context

    def __rand__(self, other: any) -> any:
        return other & self._context

    def __rxor__(self, other: any) -> any:
        return other ^ self._context

    def __ror__(self, other: any) -> any:
        return other | self._context

    def __iadd__(self, other: any) -> any:
        self._context += other
        return self._context

    def __isub__(self, other: any) -> any:
        self._context -= other
        return self._context

    def __imul__(self, other: any) -> any:
        self._context *= other
        return self._context

    def __itruediv__(self, other: any) -> any:
        self._context /= other
        return self._context

    def __ifloordiv__(self, other: any) -> any:
        self._context //= other
        return self._context

    def __imod__(self, other: any) -> any:
        self._context %= other
        return self._context

    def __ipow__(self, other: any) -> any:
        self._context **= other
        return self._context

    def __ilshift__(self, other: any) -> any:
        self._context <<= other
        return self._context

    def __irshift__(self, other: any) -> any:
        self._context >>= other
        return self._context

    def __iand__(self, other: any) -> any:
        self._context &= other
        return self._context

    def __ixor__(self, other: any) -> any:
        self._context ^= other
        return self._context

    def __ior__(self, other: any) -> any:
        self._context |= other
        return self._context

    def __neg__(self) -> any:
        return -self._context

    def __pos__(self) -> any:
        return +self._context

    def __abs__(self) -> any:
        return abs(self._context)

    def __invert__(self) -> any:
        return ~self._context

    def ref(self, key: str, default: any = None, parse: bool = True) -> any:
        """ Returns the configuration value for the given key, or the given default if not found. """
        from functools import reduce

        segments = key.split('/' if '/' in key else '__')

        try:
            context = reduce(lambda c, k: c[k] if not k.isnumeric() else c[int(k)], segments, self._root)
        except (KeyError, TypeError):
            context = default

        if context and parse:
            context = self.parse(self._root, context)

        return Config(context, root=self._root)

    def parse(self, context: any, value: any, default: any = None) -> any:
        """ Parses the given value for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = value.copy() if isinstance(value, dict | list) else value

        if isinstance(result, str):
            result = self.parse_string(result, default)

        elif isinstance(result, list):
            result = self.parse_list(context, result, default)

        elif isinstance(result, dict):
            result = self.parse_dict(context, result, default)

        return result

    def parse_string(self, value: str, default: any = None) -> str:
        """ Parses the given string for configuration references, updating the values with current configuration
        values, and returning the updated copy. """
        import os

        # Process $(c|e){...} references
        matches = Config._ref_pattern.findall(value)

        for match in matches:
            ref = str(match[0]).lower()
            if ref == 'c':
                config_value = self.ref(match[1], default, True)
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(config_value))
            elif ref == 'e':
                env_value = os.getenv(match[1])
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(env_value))

        return value

    def parse_list(self, context: any, value: list, default: any = None) -> list:
        """ Parses the given list for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = []

        for item in value:
            result.append(self.parse(context, item, default))

        return result

    def parse_dict(self, context: any, value: dict, default: any = None) -> dict:
        """ Parses the given dictionary for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = {}

        for k, v in value.items():
            result[k] = self.parse(context, v, default)

        return result

    def get(self, key: str, default: any = None) -> any:
        return self._data.get(key, default)

    def set(self, key: str, value: any) -> None:
        self._data[key] = value

    def update(self, data: dict) -> None:
        self._data.update(data)

    def copy(self) -> dict:
        return self._data.copy()

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> list:
        return list(self._data.keys())

    def values(self) -> list:
        return list(self._data.values())

    def items(self) -> list:
        return list(self._data.items())

    def pop(self, key: str, default: any = None) -> any:
        return self._data.pop(key, default)

    def json(self, context: any = None, flat: bool = True):
        import json
        if context is None:
            context = self._context
        return '{}' if context is None else json.dumps(context, indent=None if flat else 4)

    def yaml(self, context: any = None):
        import yaml
        if context is None:
            context = self._context
        return '' if context is None else yaml.dump(context, indent=4)
