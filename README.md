# kappacrypt
Offline file crypting utility using RSA + AES for Python. It allows offline encrypting files (like ransomware does). It means that you don't have to store decryption key while encrypting (some ransomware uses that mechanism). You can look for more details [here](https://en.wikipedia.org/wiki/Offline_private_key_protocol)

# installation
python setup.py install

# usage
```python
from kappacrypt import FileCryptor
from kappacrypt.keys import RSAKeys
# encryption
fc = FileCryptor("example.mp4")
rsa = RSAKeys()
rsa.gen_keys()
rsa.dump() # keys will be dumped to current directory
fc.encrypt(rsa.public_key)
    
# decryption
fc = FileCryptor("example.mp4.encrypted")
rsa = RSAKeys()
rsa.load(
    {"private_key": "path to rsa private key"}
)
fc.decrypt(rsa.private_key)

#You can also dump keys to specifed directory by using
rsa.dump({"private_key": "path to rsa private key",
          "public_key": "path to rsa public key"})
  ```
