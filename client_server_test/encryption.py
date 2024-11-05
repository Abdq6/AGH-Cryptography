from Pyfhel import Pyfhel, PyCtxt
import numpy as np

class EncryptionHandler:
    def __init__(self, scheme: str):
        self.HE = Pyfhel()
        self.scheme = scheme.upper()
        if self.scheme == 'BGV':
            self.HE.contextGen(scheme='BGV', n=2**13, t=65537, sec=128)
        elif self.scheme == 'BFV':
            self.HE.contextGen(scheme='BFV', n=2**13, t=65537, sec=128)
        elif self.scheme == 'CKKS':
            self.HE.contextGen(scheme='CKKS', n=2**14, scale=2**30, qi_sizes=[60, 40, 40, 60])
        else:
            raise ValueError("Nieznany schemat szyfrowania.")
        self.HE.keyGen()

    def encrypt(self, value):
        if self.scheme in ['BGV', 'BFV']:
            plaintext = np.array([value], dtype=np.int64)
            if self.scheme == 'BGV':
                ciphertext = self.HE.encryptBGV(plaintext)
            else:
                ciphertext = self.HE.encryptInt(plaintext)
        elif self.scheme == 'CKKS':
            plaintext = np.array([value], dtype=np.float64)
            ciphertext = self.HE.encryptFrac(plaintext)
        return ciphertext.to_bytes()

    def decrypt(self, ciphertext_bytes):
        ciphertext = PyCtxt(pyfhel=self.HE, bytestring=ciphertext_bytes)
        if self.scheme in ['BGV', 'BFV']:
            if self.scheme == 'BGV':
                decrypted = self.HE.decryptBGV(ciphertext)
            else:
                decrypted = self.HE.decryptInt(ciphertext)
            return decrypted[0]
        elif self.scheme == 'CKKS':
            decrypted = self.HE.decryptFrac(ciphertext)
            return decrypted[0]

    def serialize_public_key(self):
        return self.HE.to_bytes_public_key()

    def load_public_key(self, public_key_bytes):
        self.HE.from_bytes_public_key(public_key_bytes)
