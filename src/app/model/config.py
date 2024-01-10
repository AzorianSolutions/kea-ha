import re


class Config:
    """A class for interfacing with configuration data in object-like syntax with value variable parsing."""

    _cache: dict = {}
    """A cache of Config instances."""

    _root: any = {}
    """The root context reference."""

    _context: any = {}
    """The current context reference."""

    _debug: bool = False
    """Whether debug output is enabled."""

    _parsing: bool = True
    """Whether variable reference parsing is enabled."""

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

    @context.setter
    def context(self, value: any) -> None:
        """Sets the context of the object."""
        self.__dict__['_context'] = value

    @property
    def debug(self) -> bool:
        """Returns whether debug output is enabled."""
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        """Sets whether debug output is enabled."""
        self.__dict__['_debug'] = value

    @property
    def parsing(self) -> bool:
        """Returns whether variable reference parsing is enabled."""
        return self._parsing

    @parsing.setter
    def parsing(self, value: bool) -> None:
        """Sets whether variable reference parsing is enabled."""
        self.__dict__['_parsing'] = value

    def _log(self, label: str, message: str = None) -> None:
        """ Logs the given message to the console if debug output is enabled. """
        if self._debug:
            output = label
            if message:
                output += f': {message}'
            print(output)

    def json(self, context: any = None, flat: bool = True) -> str:
        import json

        if context is None:
            if self._context is None:
                return ''
            context = self._context

        if self.parsing:
            context = self.parse(self._root, context)

        return json.dumps(context, indent=None if flat else 4)

    def yaml(self, context: any = None) -> str:
        import yaml

        if context is None:
            if self._context is None:
                return ''
            context = self._context

        if self.parsing:
            context = self.parse(self._root, context)

        return yaml.dump(context, indent=4)

    def _convert_key(self, key: str, standard: str = '___') -> str:
        """ Converts the given key to the internal reference separators. """
        separators = ['.', '//', '/', '__']

        for separator in separators:
            if separator in key:
                return key.replace(separator, standard)

        return key

    def ref(self, context: any, key: str, default: any = None, parse: bool = True) -> any:
        """ Returns the configuration value for the given key, or the given default if not found. """
        from functools import reduce

        separator = '___'
        cache_key = self._convert_key(key, separator)

        if self.debug:
            print(f'Cache Key: {cache_key}')
            print(self._cache)

        if cache_key in self._cache:
            if self.debug:
                print(f'Cache Hit: {cache_key}')
            return self._cache[cache_key]

        ref = default

        try:
            ref = reduce(lambda c, k: c[k] if not k.isnumeric() else c[int(k)], key.split(separator), context)
        except (KeyError, TypeError):
            pass

        if ref and parse:
            ref = self.parse(context, ref)

        self._cache[cache_key] = Config(root=context, context=ref, debug=self.debug, parsing=self.parsing)

        return self._cache[cache_key]

    def parse(self, context: any, value: any, default: any = None) -> any:
        """ Parses the given value for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        if isinstance(value, str):
            return self.parse_string(context, value, default)

        elif isinstance(value, dict):
            return self.parse_dict(context, value, default)

        elif isinstance(value, list):
            return self.parse_list(context, value, default)

        return value

    def parse_dict(self, context: any, value: dict, default: any = None) -> dict:
        """ Parses the given dictionary for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = {}

        for k, v in value.items():
            result[k] = self.parse(context, v, default)

        return result

    def parse_list(self, context: any, value: list, default: any = None) -> list:
        """ Parses the given list for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = []

        for item in value:
            result.append(self.parse(context, item, default))

        return result

    def parse_string(self, context: any, value: str, default: any = None) -> str:
        """ Parses the given string for configuration references, updating the values with current configuration
        values, and returning the updated copy. """
        import os

        # Process $(c|e){...} references
        matches = Config._ref_pattern.findall(value)

        for match in matches:
            ref = str(match[0]).lower()

            if ref == 'c':
                config_value = self.ref(context=context, key=match[1], default=default, parse=self.parsing)
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(config_value))

            elif ref == 'e':
                env_value = os.getenv(match[1])
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(env_value))

        return value

    def __init__(self, root: any, context: any = None, debug: bool = False, parsing: bool = True):
        if context is None and root is not None:
            context = root
        self.__dict__['_cache'] = {}
        self.__dict__['_root'] = root
        self.__dict__['_context'] = context
        self.__dict__['_debug'] = debug
        self.__dict__['_parsing'] = parsing

    def __call__(self, key: str = None, default: any = None):
        self._log('Config.__call__', key)
        if key is None:
            return self._context
        return self.ref(self._root, key, default=default, parse=self.parsing)

    def __getattr__(self, key: str) -> any:
        self._log('Config.__getattr__', key)

        if key in self.__dict__:
            return self.__dict__[key]

        # return self.ref(context=self._root, key=key, default=None, parse=self.parsing)

        if key not in self._cache:
            context = {}

            if key in self._context:
                context = self._context[key]

            if self.parsing:
                context = self.parse(self._root, context)

            self._cache[key] = Config(root=self._root, context=context, debug=self.debug, parsing=self.parsing)

        return self._cache[key]

    def __setattr__(self, key: str, value: any) -> None:
        self._log('Config.__setattr__', key)

        test_keys = [key]

        if not key.startswith('_'):
            test_keys.append(f'_{key}')

        for test_key in test_keys:
            if test_key not in self.__dict__:
                continue

            if callable(ref := self.__dict__[test_key]):
                ref(value)
                return

            self.__dict__[test_key] = value
            return

        self._context[key] = value

    def __delattr__(self, key: str) -> None:
        self._log('Config.__delattr__', key)

        if key in self.__dict__:
            del self.__dict__[key]
            return

        del self._context[key]

    def __getitem__(self, key: str) -> any:
        self._log('Config.__getitem__', key)

        if key in self.__dict__:
            return self.__dict__[key]

        if key not in self._cache:
            context = {}

            if key in self._context:
                context = self._context[key]

            if self.parsing:
                context = self.parse(self._root, context)

            if '.' in key or '/' in key or '__' in key:
                return self.ref(context=self._root, key=key, default=None, parse=self.parsing)

            self._cache[key] = Config(root=self._root, context=context, debug=self.debug, parsing=self.parsing)

        return self._cache[key]

    def __setitem__(self, key: str, value: any) -> None:
        self._log('Config.__setitem__', key)

        if key in self.__dict__:
            self.__dict__[key] = value
            return

        self[key].context = value

    def __delitem__(self, key: str) -> None:
        self._log('Config.__delitem__', key)
        del self._context[key]

    def __contains__(self, key: str) -> bool:
        return key in self._context

    def __iter__(self):
        return iter(self._context)

    def get(self, key: str, default: any = None) -> any:
        return self._context.get(key, default)

    def set(self, key: str, value: any) -> None:
        self._context[key] = value

    def update(self, data: dict) -> None:
        self._context.update(data)

    def copy(self) -> dict:
        return self._context.copy()

    def clear(self) -> None:
        self._context.clear()

    def keys(self) -> list:
        return list(self._context.keys())

    def values(self) -> list:
        return list(self._context.values())

    def items(self) -> list:
        return list(self._context.items())

    def pop(self, key: str, default: any = None) -> any:
        return self._context.pop(key, default)

    def __len__(self):
        return len(self._context)

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

    def __repr__(self):
        return self.yaml()

    def __str__(self):
        if not self.parsing:
            return str(self._context)

        ref = self.parse(self._root, self._context)

        if isinstance(ref, dict) or isinstance(ref, list):
            return self.yaml(ref)

        return str(ref)

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
