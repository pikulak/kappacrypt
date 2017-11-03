from os import urandom

from Cryptodome.PublicKey import RSA

from kappacrypt.utils import (
    ensure_valid_keypaths,
    write_to_file,
    read_from_file
)


class RSAKeys:

    DEFAULT_PUBLIC_KEY_PATH = "public_key.der"
    DEFAULT_PRIVATE_KEY_PATH = "private_key.der"
    DEFAULT_KEYS_PATHS = {
        "public_key": DEFAULT_PUBLIC_KEY_PATH,
        "private_key": DEFAULT_PRIVATE_KEY_PATH
    }

    def __init__(self):

        self._private_key = None
        self._public_key = None
        self._key_size = 4096

    def gen_keys(self):

        key = RSA.generate(self._key_size, urandom)
        private_key = key.exportKey()
        public_key = key.publickey().exportKey()
        self._private_key, self._public_key = private_key, public_key

    @property
    def public_key(self):

        if not self._public_key:
            self.gen_keys()
        return self._public_key

    @property
    def private_key(self):

        if not self._private_key:
            self.gen_keys()
        return self._private_key

    def keys_exists(self):

        if not self._private_key and not self._public_key:
            return False
        else:
            return True

    def dump(self, to_paths=None):

        if not to_paths:
                to_paths = self.DEFAULT_KEYS_PATHS

        if not self.keys_exists():
            raise ValueError("Keys were not loaded or generated. \
                              Did you forgot to use RSAKeys.gen_keys() or RSAKeys.load() methods?")

        if "private_key" in to_paths:
            write_to_file(to_paths["private_key"], 'wb', self._private_key)

        if "public_key" in to_paths:
            write_to_file(to_paths["public_key"], 'wb', self._public_key)

    def load(self, from_paths=None):
        
        if not from_paths:
            from_paths = self.DEFAULT_KEYS_PATHS

        ensure_valid_keypaths(from_paths)

        if "private_key" in from_paths:
            self._private_key = read_from_file(from_paths["private_key"], 'rb')

        if "public_key" in from_paths:
            self._public_key = read_from_file(from_paths["public_key"], 'rb')

    def load_directly(self, key_data, key_type):

        if key_type == "public_key":
            self._public_key = key_data

        if key_type == "private_key":
            self._private_key = key_data
