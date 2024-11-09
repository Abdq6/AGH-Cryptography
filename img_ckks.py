from Pyfhel import Pyfhel
import cv2
import numpy as np
import os

# Parametry
input_path = "./Tests/Input/random_image.jpg"
output_path = "./Tests/Output/random_image_gray.jpg"

# Wczytanie obrazu
image = cv2.imread(input_path)
if image is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu pod ścieżką {input_path}")

# Wymiary obrazu
height, width, _ = image.shape
num_pixels = height * width

# Konfiguracja Pyfhel dla CKKS
HE = Pyfhel()
HE.contextGen(scheme="CKKS", n=2**15, scale=2**40, qi_sizes=[60, 40, 40, 60])
HE.keyGen()

# Współczynniki do konwersji na skalę szarości
weights = {
    "R": 0.2989,
    "G": 0.5870,
    "B": 0.1140,
}

# Rozdzielenie kanałów i spłaszczenie
R, G, B = cv2.split(image)
flat_R = R.flatten().astype(np.float64)
flat_G = G.flatten().astype(np.float64)
flat_B = B.flatten().astype(np.float64)

# Sprawdzenie liczby slotów
n_slots = HE.get_nSlots()
if num_pixels > n_slots:
    raise ValueError(f"Liczba pikseli ({num_pixels}) przekracza liczbę dostępnych slotów ({n_slots}).")

# Szyfrowanie kanałów
ctxt_R = HE.encryptFrac(flat_R)
ctxt_G = HE.encryptFrac(flat_G)
ctxt_B = HE.encryptFrac(flat_B)

# Kodowanie współczynników jako plaintextów
encoded_weights = {
    key: HE.encodeFrac(np.full(n_slots, value, dtype=np.float64)) for key, value in weights.items()
}

# Operacje homomorficzne
weighted_R = ctxt_R * encoded_weights["R"]
weighted_G = ctxt_G * encoded_weights["G"]
weighted_B = ctxt_B * encoded_weights["B"]
ctxt_gray = weighted_R + weighted_G + weighted_B

# Odszyfrowanie
decrypted_gray = HE.decryptFrac(ctxt_gray)

# Przycięcie wektora do rozmiaru obrazu
trimmed_gray = decrypted_gray[:num_pixels]

# Przeskalowanie do zakresu [0, 255] i konwersja do uint8
gray_image = np.clip(trimmed_gray, 0, 255).astype(np.uint8)

# Rekonstrukcja obrazu
gray_image = gray_image.reshape((height, width))

# Tworzenie folderu wyjściowego, jeśli nie istnieje
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Zapis obrazu wynikowego
cv2.imwrite(output_path, gray_image)
print(f"Zapisano przetworzony obraz do {output_path}")
