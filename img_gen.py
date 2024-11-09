from PIL import Image
import numpy as np
import os

# Ustawienia
output_folder = './Tests/Input/'
output_filename = 'random_image.jpg'
output_path = os.path.join(output_folder, output_filename)

# Tworzenie folderu, jeśli nie istnieje
os.makedirs(output_folder, exist_ok=True)

# Definicja wyraźnie różniących się kolorów
distinct_colors = [
    (255, 0, 0),    # Czerwony
    (0, 255, 0),    # Zielony
    (0, 0, 255),    # Niebieski
    (255, 255, 0),  # Żółty
    (0, 255, 255),  # Cyjan
    (255, 0, 255),  # Magenta
    (128, 0, 0),    # Bordowy
    (0, 128, 0),    # Ciemnozielony
    (0, 0, 128),    # Granatowy
    (128, 128, 0),  # Oliwkowy
    (0, 128, 128),  # Teal
    (128, 0, 128),  # Fioletowy
    (192, 192, 192),# Srebrny
    (128, 128, 128),# Szary
    (0, 0, 0),      # Czarny
    (255, 255, 255) # Biały
]

# Rozmiar obrazu
width, height = 25, 25

# Inicjalizacja tablicy pikseli
pixels = np.zeros((height, width, 3), dtype=np.uint8)

# Wypełnianie obrazu losowymi kolorami z listy distinct_colors
for y in range(height):
    for x in range(width):
        pixels[y, x] = distinct_colors[np.random.randint(len(distinct_colors))]

# Tworzenie obrazu z tablicy pikseli
image = Image.fromarray(pixels, 'RGB')

# Zapisywanie obrazu w formacie JPEG
image.save(output_path, 'JPEG')

print(f'Obraz z wyraźnymi kolorami został zapisany w: {output_path}')
