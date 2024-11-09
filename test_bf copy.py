from Pyfhel import Pyfhel
import cv2
import numpy as np

# Ścieżki do plików
input_path = "./Tests/Input/a.jpg"
output_path = "./Tests/Output/a_gray.jpg"

# Wczytanie obrazu
image = cv2.imread(input_path)

if image is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu pod ścieżką {input_path}")

# Konfiguracja Pyfhel
HE = Pyfhel()
HE.contextGen(scheme="BFV", n=2**14, t=65537)
HE.keyGen()

# Znormalizowanie współczynników (skalowanie dla BFV/BGV)
scale_factor = 1000
weights = {
    "R": int(0.2989 * scale_factor),
    "G": int(0.5870 * scale_factor),
    "B": int(0.1140 * scale_factor),
}

# Podział obrazu na kanały
B, G, R = cv2.split(image)

# Szyfrowanie kanałów
encrypted_B = np.array([[HE.encrypt(int(pixel)) for pixel in row] for row in B], dtype=object)
encrypted_G = np.array([[HE.encrypt(int(pixel)) for pixel in row] for row in G], dtype=object)
encrypted_R = np.array([[HE.encrypt(int(pixel)) for pixel in row] for row in R], dtype=object)

# Przekształcenie na skalę szarości na zaszyfrowanych danych
encrypted_gray = np.array([
    [
        HE.add(
            HE.add(
                HE.mult(encrypted_R[i][j], weights["R"]),
                HE.mult(encrypted_G[i][j], weights["G"])
            ),
            HE.mult(encrypted_B[i][j], weights["B"])
        )
        for j in range(image.shape[1])
    ]
    for i in range(image.shape[0])
], dtype=object)

# Odszyfrowanie szarości
decrypted_gray = np.array([
    [
        HE.decryptInt(pixel) for pixel in row
    ]
    for row in encrypted_gray
])

# Przywrócenie zakresu pikseli (skalowanie z powrotem)
reconstructed_image = (np.array(decrypted_gray) / scale_factor).astype(np.uint8)

# Zapis obrazu wynikowego
cv2.imwrite(output_path, reconstructed_image)

print(f"Zapisano przetworzony obraz do {output_path}")
