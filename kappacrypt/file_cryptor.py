import struct
import os

from Cryptodome.Cipher import AES

from kappacrypt.keys import AESKey
from kappacrypt.core import KeysChunk


class FileCryptor:

    def __init__(self, path):

        self._path = path
        self._file_size = os.path.getsize(self._path)
        self._keys_chunk = None
        self.chunksize = 64*1024

    @property
    def keys_chunk(self):

        if not self._keys_chunk:
            self.load_keys_chunk()

        return self._keys_chunk

    def encrypt(self, rsa_public_key, out_file_path=None):

        if not out_file_path:
            out_file_path = self._path + ".encrypted"

        aes_key = AESKey()
        aes_encryptor = AES.new(aes_key.key,
                                aes_key.mode, 
                                IV=aes_key.IV)
        keys_chunk = KeysChunk(aes_key, rsa_public_key).compute()

        with open(self._path, 'rb') as plain_file:
            with open(out_file_path, 'wb') as encrypted_file:
                encrypted_file.write(struct.pack('>Q', self._file_size))
                encrypted_file.write(keys_chunk)

                while True:
                    chunk = plain_file.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b'\x00' * (16 - len(chunk) % 16)
                    encrypted_file.write(aes_encryptor.encrypt(chunk))

    def decrypt(self, rsa_private_key, out_file_path=None):

        if not self._keys_chunk:
            self.load_keys_chunk()

        if not out_file_path:
            out_file_path = os.path.splitext(self._path)[0]

        self._keys_chunk.aes_key.decrypt(rsa_private_key)

        decryptor = AES.new(self._keys_chunk.aes_key.key, 
                            self._keys_chunk.aes_key.mode, 
                            IV=self._keys_chunk.aes_key.IV)

        with open(self._path, 'rb') as encrypted_file:
            original_file_size = self.get_original_file_size(encrypted_file)
            encrypted_file.seek(16 + 512 + 8)
            with open(out_file_path, 'wb') as decrypted_file:
                while True:
                    chunk = encrypted_file.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    decrypted_file.write(decryptor.decrypt(chunk))

                decrypted_file.truncate(original_file_size)

    @staticmethod
    def get_original_file_size(file_object):
        struct_q_size = struct.calcsize('Q')
        struct_q_value = file_object.read(struct_q_size)
        original_file_size = struct.unpack('>Q', struct_q_value)[0]
        return original_file_size

    def load_keys_chunk(self):

        with open(self._path, 'rb') as encrypted_file:
            self._keys_chunk = KeysChunk()
            self._keys_chunk.load(encrypted_file.read(16 + 512 + 8))
