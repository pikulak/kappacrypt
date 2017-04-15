from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class AESKey:

	def __init__(self, key=None, IV=None, encrypted=False):

		self._key = key
		self._IV = IV
		self._mode = AES.MODE_CBC
		self.encrypted = encrypted

	@property
	def key(self):

		if not self._key:
			self._key = Random.get_random_bytes(32)
		
		return self._key

	@property
	def IV(self):

		if not self._IV:
			self._IV = Random.get_random_bytes(16)
		
		return self._IV

	@property
	def mode(self):

		return self._mode

	def decrypt(self, rsa_private_key):

		if self.encrypted:
			key_obj = RSA.importKey(rsa_private_key)
			cipher = PKCS1_OAEP.new(key_obj)
			self._key = cipher.decrypt(self._key)
