import re


class Reflective(dict):
    """A class for working with dynamically referenced nested data structures."""

    _ref: any = None
    """A reference to the current configuration value."""

    _parent: 'Reflective' = None
    """A reference to the parent Reflective instance."""

    _key: str = None
    """The parent context key."""

    _debug: bool = False
    """Whether debug output is enabled."""

    _parsing: bool = True
    """Whether variable reference parsing is enabled."""

    _properties: list = ['ref', 'root', 'parent', 'key', 'debug', 'parsing']
    """The list of properties to be treated as static by the __getattr__ and __setattr__ methods."""

    _ref_pattern = re.compile(r'\$(c|e){([a-z0-9_/]+)}', re.IGNORECASE)
    """ The regular expression pattern used to match variable references in values. """

    @property
    def ref(self) -> any:
        """Returns the configuration value reference of the object."""
        if '_ref' not in self.__dict__:
            self.__dict__['_ref'] = None
        return self.__dict__['_ref']

    @ref.setter
    def ref(self, value: any) -> None:
        """Sets the configuration value reference of the object."""
        self.__dict__['_ref'] = value

    @property
    def ref_path(self) -> list:
        """Returns the path to the current configuration value."""
        path = []
        ref = self

        if self.key:
            path.insert(0, self.key)

        while ref.parent:
            ref = ref.parent
            # If the parent has a key, prepend the parent key to the path
            if ref.key:
                path.insert(0, ref.key)

        return path

    @property
    def root(self) -> 'Reflective' or None:
        """Returns the root Reflective instance of the object."""
        if isinstance(self.parent, Reflective):
            return self.parent.root
        return self

    @property
    def parent(self) -> 'Reflective' or None:
        """Returns the parent context of the object."""
        if '_parent' not in self.__dict__:
            self.__dict__['_parent'] = None
        return self.__dict__['_parent']

    @parent.setter
    def parent(self, value: 'Reflective' or None) -> None:
        """Sets the parent context of the object."""
        self.__dict__['_parent'] = value

    @property
    def key(self) -> str | None:
        """Returns the context key for this object within it's parent object."""
        if '_key' not in self.__dict__:
            self.__dict__['_key'] = None
        return self.__dict__['_key']

    @key.setter
    def key(self, value: str) -> None:
        """Sets the context key for this object within it's parent object."""
        self.__dict__['_key'] = value

    @property
    def debug(self) -> bool:
        """Returns whether debug output is enabled."""
        if self.root != self:
            return self.root.debug
        if '_debug' not in self.__dict__:
            self.__dict__['_debug'] = False
        return self.__dict__['_debug']

    @debug.setter
    def debug(self, value: bool) -> None:
        """Sets whether debug output is enabled."""
        if self.root != self:
            self.root.debug = value
            return
        self.__dict__['_debug'] = value

    @property
    def parsing(self) -> bool:
        """Returns whether variable reference parsing is enabled."""
        if self.root != self:
            return self.root.parsing
        if '_parsing' not in self.__dict__:
            self.__dict__['_parsing'] = True
        return self.__dict__['_parsing']

    @parsing.setter
    def parsing(self, value: bool) -> None:
        """Sets whether variable reference parsing is enabled."""
        if self.root != self:
            self.root.parsing = value
            return
        self.__dict__['_parsing'] = value

    @property
    def simple(self) -> bool:
        """Returns whether the current configuration value is a simple value."""
        return not isinstance(self.ref, dict) and not isinstance(self.ref, list)

    def __repr__(self) -> str:
        return f'<Reflective>: {self.__str__}'

    def __str__(self):
        if isinstance(self._ref, dict) or isinstance(self._ref, list):
            return self.json(self._ref)
        return str(self._ref)

    def __bool__(self):
        return bool(self._ref)

    def __int__(self):
        return int(self._ref)

    def __float__(self):
        return float(self._ref)

    def __complex__(self) -> any:
        return complex(self._ref)

    def __bytes__(self):
        return bytes(self._ref)

    def __hash__(self):
        return hash(self._ref)

    def __iter__(self):
        return iter(self._ref)

    def __init__(self, ref: any, parent: 'Reflective' or None = None, key: str or None = None):
        super().__init__()
        self.ref = ref
        if parent:
            self.parent = parent
        if key:
            self.key = key

    def __call__(self, key: any = None, default: any = None) -> any:
        self._log('Config.__call__', key)

        if self.simple and key is not None:
            self.parent.up(self.key, key)
            return self

        # If called with no arguments, return the current value
        if key is None:
            return self

        return self.create(key=key, default=default, parse=self.parsing)

    def __getattr__(self, key: str) -> any:
        self._log('Config.__getattr__', key)
        if key in self._properties + list(self.__dict__.keys()):
            self._log(f'Config.__getattr__', f'{key} is a property')
            return super().__getattribute__(key)
        return self.create(key=key, default=None, parse=self.parsing)

    def __setattr__(self, key: str, value: any) -> None:
        self._log('Config.__setattr__', key)
        internal = list(self.__dict__.keys())

        if key in self._properties:
            super().__setattr__(key, value)
            return

        elif key in internal:
            self.__dict__[key] = value
            return

        elif (private_key := f'_{key}') in internal:
            self.__dict__[private_key] = value
            return

        if self.ref is not None and key is not None and key in self.ref:
            self.up(key, value)

    def __delattr__(self, key: str) -> None:
        self._log('Config.__delattr__', key)

        if key in self.__dict__:
            del self.__dict__[key]
            return

        del self.ref[key]

    def __getitem__(self, key: str) -> any:
        self._log('Config.__getitem__', key)
        if key in self.__dict__:
            return self.__dict__[key]
        return self.create(key=key, default=None, parse=self.parsing)

    def __setitem__(self, key: str, value: any) -> None:
        self._log('Config.__setitem__', key)

        if key in self.__dict__:
            self.__dict__[key] = value
            return

        if self.ref is not None and key is not None:
            self.up(key, value)

    def __delitem__(self, key: str) -> None:
        self._log('Config.__delitem__', key)

        if key in self.__dict__:
            del self.__dict__[key]
            return

        del self.ref[key]

    def __reversed__(self):
        return reversed(self._ref)

    def __contains__(self, key: str) -> bool:
        return key in self._ref

    def __missing__(self, key: str) -> any:
        return self._ref.__missing__(key)

    def __enter__(self):
        return self._ref.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._ref.__exit__(exc_type, exc_val, exc_tb)

    def __del__(self):
        if hasattr(self.ref, '__del__'):
            return self._ref.__del__()
        return

    def __len__(self):
        return len(self._ref)

    def __sizeof__(self):
        return self._ref.__sizeof__()

    def __dir__(self):
        return dir(self._ref)

    def __format__(self, format_spec: str):
        return self._ref.__format__(format_spec)

    def __lt__(self, other: any) -> bool:
        return self._ref < other

    def __le__(self, other: any) -> bool:
        return self._ref <= other

    def __eq__(self, other: any) -> bool:
        return self._ref == other

    def __ne__(self, other: any) -> bool:
        return self._ref != other

    def __gt__(self, other: any) -> bool:
        return self._ref > other

    def __ge__(self, other: any) -> bool:
        return self._ref >= other

    def __add__(self, other: any) -> any:
        return self._ref + other

    def __sub__(self, other: any) -> any:
        return self._ref - other

    def __mul__(self, other: any) -> any:
        return self._ref * other

    def __truediv__(self, other: any) -> any:
        return self._ref / other

    def __floordiv__(self, other: any) -> any:
        return self._ref // other

    def __mod__(self, other: any) -> any:
        return self._ref % other

    def __divmod__(self, other: any) -> any:
        return divmod(self._ref, other)

    def __pow__(self, other: any) -> any:
        return self._ref ** other

    def __lshift__(self, other: any) -> any:
        return self._ref << other

    def __rshift__(self, other: any) -> any:
        return self._ref >> other

    def __and__(self, other: any) -> any:
        return self._ref & other

    def __xor__(self, other: any) -> any:
        return self._ref ^ other

    def __or__(self, other: any) -> any:
        return self._ref | other

    def __radd__(self, other: any) -> any:
        return other + self._ref

    def __rsub__(self, other: any) -> any:
        return other - self._ref

    def __rmul__(self, other: any) -> any:
        return other * self._ref

    def __rtruediv__(self, other: any) -> any:
        return other / self._ref

    def __rfloordiv__(self, other: any) -> any:
        return other // self._ref

    def __rmod__(self, other: any) -> any:
        return other % self._ref

    def __rdivmod__(self, other: any) -> any:
        return divmod(other, self._ref)

    def __rpow__(self, other: any) -> any:
        return other ** self._ref

    def __rlshift__(self, other: any) -> any:
        return other << self._ref

    def __rrshift__(self, other: any) -> any:
        return other >> self._ref

    def __rand__(self, other: any) -> any:
        return other & self._ref

    def __rxor__(self, other: any) -> any:
        return other ^ self._ref

    def __ror__(self, other: any) -> any:
        return other | self._ref

    def __iadd__(self, other: any) -> any:
        self._ref += other
        return self._ref

    def __isub__(self, other: any) -> any:
        self._ref -= other
        return self._ref

    def __imul__(self, other: any) -> any:
        self._ref *= other
        return self._ref

    def __itruediv__(self, other: any) -> any:
        self._ref /= other
        return self._ref

    def __ifloordiv__(self, other: any) -> any:
        self._ref //= other
        return self._ref

    def __imod__(self, other: any) -> any:
        self._ref %= other
        return self._ref

    def __ipow__(self, other: any) -> any:
        self._ref **= other
        return self._ref

    def __ilshift__(self, other: any) -> any:
        self._ref <<= other
        return self._ref

    def __irshift__(self, other: any) -> any:
        self._ref >>= other
        return self._ref

    def __iand__(self, other: any) -> any:
        self._ref &= other
        return self._ref

    def __ixor__(self, other: any) -> any:
        self._ref ^= other
        return self._ref

    def __ior__(self, other: any) -> any:
        self._ref |= other
        return self._ref

    def __neg__(self) -> any:
        return -self._ref

    def __pos__(self) -> any:
        return +self._ref

    def __abs__(self) -> any:
        return abs(self._ref)

    def __invert__(self) -> any:
        return ~self._ref

    def get(self, key: str, default: any = None) -> any:
        return self._ref.get(key, default)

    def set(self, key: str, value: any) -> None:
        self._ref[key] = value

    def update(self, data: dict) -> None:
        self._ref.update(data)

    def copy(self) -> dict:
        return self._ref.copy()

    def clear(self) -> None:
        self._ref.clear()

    def keys(self) -> list:
        return list(self._ref.keys())

    def values(self) -> list:
        return list(self._ref.values())

    def items(self) -> list:
        return list(self._ref.items())

    def pop(self, key: str, default: any = None) -> any:
        return self._ref.pop(key, default)

    def popitem(self) -> tuple:
        return self._ref.popitem()

    def json(self, ref: any = None, flat: bool = True) -> str:
        import json

        if ref is None:
            if self.ref is None:
                return ''
            ref = self.ref

        if self.parsing:
            ref = self.parse(ref)

        return json.dumps(ref, indent=None if flat else 4)

    def yaml(self, ref: any = None) -> str:
        import yaml

        if ref is None:
            if self.ref is None:
                return ''
            ref = self.ref

        if self.parsing:
            ref = self.parse(ref)

        return yaml.dump(ref, indent=4)

    def create(self, key: str, default: any = None, parse: bool = True, context: any = None) -> 'Reflective':
        """ Returns the Reflective instance for the configuration value for the given key, or the given default if not
        found. """
        from functools import reduce

        if context is None:
            context = self.ref

        ref = default
        segments = self._get_key_segments(key)

        try:
            ref = reduce(self._reducer, segments, context)
        except (KeyError, TypeError):
            pass

        if ref and parse:
            ref = self.parse(ref)

        return Reflective(ref=ref, parent=self, key=segments[-1])

    def up(self, key: str or int, value: any, context: any = None) -> 'Reflective':
        """ Updates the configuration value for the given key within the given context. """
        from functools import reduce
        self._log('Config.up', key)

        if context is None:
            context = self.ref

        segments = self._get_key_segments(key)

        if self.parent is not None:
            ref = reduce(self._reducer, segments, self)
            return self.root.up('/'.join(str(x) for x in ref.ref_path), value, context)

        if len(segments) == 1:
            self.ref[segments[0]] = value
            return self

        ref = self.ref

        try:
            ref = reduce(self._reducer, segments[:-1], ref)
            found = True
        except (KeyError, TypeError):
            found = False

        if found:
            ref_key = segments[-1]

            if isinstance(ref, list) and ref_key.isnumeric():
                ref_key = int(ref_key)

            ref[ref_key] = value

        return self

    def parse(self, value: any, default: any = None) -> any:
        """ Parses the given value for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        if isinstance(value, str):
            return self.parse_string(value, default)

        elif isinstance(value, dict):
            return self.parse_dict(value, default)

        elif isinstance(value, list):
            return self.parse_list(value, default)

        return value

    def parse_dict(self, value: dict, default: any = None) -> dict:
        """ Parses the given dictionary for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = {}

        for k, v in value.items():
            result[k] = self.parse(v, default)

        return result

    def parse_list(self, value: list, default: any = None) -> list:
        """ Parses the given list for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = []

        for item in value:
            result.append(self.parse(item, default))

        return result

    def parse_string(self, value: str, default: any = None) -> str:
        """ Parses the given string for configuration references, updating the values with current configuration
        values, and returning the updated copy. """
        import os

        # Process $(c|e){...} references
        matches = Reflective._ref_pattern.findall(value)

        for match in matches:
            ref = str(match[0]).lower()

            if ref == 'c':
                new_value = self.create(key=match[1], default=default, parse=self.parsing, context=self.root.ref)
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(new_value))

            elif ref == 'e':
                new_value = os.getenv(match[1])
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(new_value))

        return value

    def _convert_key(self, key: str, standard: str = '___') -> str:
        """ Converts the given key to the internal reference separators. """
        separators = ['.', '//', '/', '__']

        for separator in separators:
            if separator in key:
                return key.replace(separator, standard)

        return key

    def _get_key_segments(self, key: str or int) -> list:
        """ Parses the given key and returns a list of segments. """
        if isinstance(key, int):
            return [key]

        separators = ['//', '/', '__', '.']

        for separator in separators:
            if separator in key:
                return key.split(separator)

        return [key]

    def _log(self, label: str, message: str = None) -> None:
        """ Logs the given message to the console if debug output is enabled. """
        if self.debug:
            output = label
            if message:
                output += f': {message}'
            print(output)

    def _reduce(self, ref: any, key: str) -> tuple[bool, any]:
        """ Reduces the given reference based on the given key. """
        from functools import reduce

        segments = self._get_key_segments(key)

        try:
            ref = reduce(self._reducer, segments, ref)
            found = True
        except (KeyError, TypeError):
            found = False

        return found, ref

    def _reducer(self, c, k) -> any:
        """ Reduces the given reference based on the given key. """
        if not isinstance(k, int) and not str(k).isnumeric():
            return c[k]
        return c[int(k)]
