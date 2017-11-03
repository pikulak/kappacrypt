from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

from kappacrypt.keys import AESKey


class KeysChunk:

    def __init__(self, aes_key=None, rsa_public_key=None):

        self._aes_key = aes_key
        self._rsa_public_key = rsa_public_key

    @property
    def aes_key(self):
        return self._aes_key

    def compute(self):

        cipher = PKCS1_OAEP.new(RSA.importKey(self._rsa_public_key))
        encrypted_aes_key = cipher.encrypt(self._aes_key.key)
        chunk = self._aes_key.IV
        chunk += encrypted_aes_key
        return chunk

    def load(self, chunk):
        IV = chunk[8:24]
        encrypted_aes_key = chunk[24:512+24]
        
        self._aes_key = AESKey(key=encrypted_aes_key, IV=IV, encrypted=True)
