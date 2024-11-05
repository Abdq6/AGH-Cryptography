import numpy as np
from Pyfhel import Pyfhel

def bgv_example():
    print("\n--- BGV Example ---")
    HE = Pyfhel()  # Inicjalizacja obiektu Pyfhel
    HE.contextGen(scheme='BGV', n=2**13, t=65537, sec=128)  # Generowanie kontekstu
    HE.keyGen()  # Generowanie kluczy

    plaintext = np.array([42], dtype=np.int64)  # Liczba całkowita do zaszyfrowania
    ciphertext = HE.encryptBGV(plaintext)  # Szyfrowanie
    decrypted = HE.decryptBGV(ciphertext)  # Odszyfrowywanie
    print("Odszyfrowana wartość BGV:", decrypted[0])

def bfv_example():
    print("\n--- BFV Example ---")
    HE = Pyfhel()  # Inicjalizacja obiektu Pyfhel
    HE.contextGen(scheme='BFV', n=2**13, t=65537, sec=128)  # Generowanie kontekstu
    HE.keyGen()  # Generowanie kluczy

    plaintext = np.array([42], dtype=np.int64)  # Liczba całkowita do zaszyfrowania
    ciphertext = HE.encryptInt(plaintext)  # Szyfrowanie
    decrypted = HE.decryptInt(ciphertext)  # Odszyfrowywanie
    print("Odszyfrowana wartość BFV:", decrypted[0])

def ckks_example():
    print("\n--- CKKS Example ---")
    HE = Pyfhel()  # Inicjalizacja obiektu Pyfhel
    # Generowanie kontekstu z dodatkowym parametrem `qi_sizes`
    HE.contextGen(scheme='CKKS', n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])
    HE.keyGen()  # Generowanie kluczy

    plaintext = np.array([3.0], dtype=np.float64)  # Liczba zmiennoprzecinkowa do zaszyfrowania
    ciphertext = HE.encryptFrac(plaintext)  # Szyfrowanie
    decrypted = HE.decryptFrac(ciphertext)  # Odszyfrowywanie
    print("Odszyfrowana wartość CKKS:", decrypted[0])

if __name__ == "__main__":
    bgv_example()
    bfv_example()
    ckks_example()
