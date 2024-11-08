import unittest
from Encryption import EncryptionHandler
from Pyfhel import PyCtxt
import numpy as np

class TestEncryptionHandler(unittest.TestCase):
    def setUp(self):
        """Przygotowanie instancji szyfrowania do testów."""
        self.bg_handler = EncryptionHandler('BGV')
        self.bf_handler = EncryptionHandler('BFV')
        self.ckks_handler = EncryptionHandler('CKKS')

    def test_encryption_decryption_bgv(self):
        """Test szyfrowania i deszyfrowania w BGV."""
        value = 42
        encrypted = self.bg_handler.encrypt(value)
        decrypted = self.bg_handler.decrypt(encrypted)
        self.assertEqual(value, decrypted, "BGV: Wynik odszyfrowania różni się od oryginału.")

    def test_encryption_decryption_bfv(self):
        """Test szyfrowania i deszyfrowania w BFV."""
        value = 42
        encrypted = self.bf_handler.encrypt(value)
        decrypted = self.bf_handler.decrypt(encrypted)
        self.assertEqual(value, decrypted, "BFV: Wynik odszyfrowania różni się od oryginału.")

    def test_encryption_decryption_ckks(self):
        """Test szyfrowania i deszyfrowania w CKKS."""
        value = 42.42
        encrypted = self.ckks_handler.encrypt(value)
        decrypted = self.ckks_handler.decrypt(encrypted)
        self.assertAlmostEqual(value, decrypted, delta=1e-5, msg="CKKS: Wynik odszyfrowania różni się od oryginału.")

    def test_homomorphic_addition_bgv(self):
        """Test homomorficznego dodawania w BGV."""
        value = 42
        ciphertext = self.bg_handler.HE.encryptBGV(np.array([value]))
        result_ciphertext = ciphertext + ciphertext
        decrypted_result = self.bg_handler.HE.decryptBGV(result_ciphertext)[0]
        self.assertEqual(value * 2, decrypted_result, "BGV: Błąd w wyniku homomorficznego dodawania.")

    def test_homomorphic_addition_bfv(self):
        """Test homomorficznego dodawania w BFV."""
        value = 42
        ciphertext = self.bf_handler.HE.encryptInt(np.array([value]))
        result_ciphertext = ciphertext + ciphertext
        decrypted_result = self.bf_handler.HE.decryptInt(result_ciphertext)[0]
        self.assertEqual(value * 2, decrypted_result, "BFV: Błąd w wyniku homomorficznego dodawania.")

    def test_homomorphic_addition_ckks(self):
        """Test homomorficznego dodawania w CKKS."""
        value = 42.42
        ciphertext = self.ckks_handler.HE.encryptFrac(np.array([value]))
        result_ciphertext = ciphertext + ciphertext
        decrypted_result = self.ckks_handler.HE.decryptFrac(result_ciphertext)[0]
        self.assertAlmostEqual(value * 2, decrypted_result, delta=1e-5, msg="CKKS: Błąd w wyniku homomorficznego dodawania.")

    def test_serialization_deserialization(self):
        """Test serializacji i deserializacji kluczy."""
        public_key_bytes = self.ckks_handler.serialize_public_key()
        new_handler = EncryptionHandler('CKKS')
        new_handler.load_public_key(public_key_bytes)
        self.assertIsNotNone(new_handler, "Nie udało się wczytać klucza publicznego po serializacji.")

if __name__ == "__main__":
    unittest.main()
