import numpy as np
from Pyfhel import Pyfhel
import os
import cv2

class EncryptionAndGrayscale:
    def __init__(self):
        self.HE = Pyfhel()
        self.context_initialized = False
        self.slot_size = 2**14
        self.scale = 2**40
        self.qi_sizes = [60, 40, 40, 60]
        self.weights = {
            "B": 0.1140,
            "G": 0.5870,
            "R": 0.2989,
        }

    def initialize_context(self):
        """Inicjalizuje kontekst Pyfhel dla szyfrowania homomorficznego."""
        if not self.context_initialized:
            self.HE.contextGen(scheme="CKKS", n=self.slot_size, scale=self.scale, qi_sizes=self.qi_sizes)
            self.HE.keyGen()
            self.context_initialized = True
            print(f"Kontekst zainicjowany z n={self.slot_size}, scale={self.scale}, qi_sizes={self.qi_sizes}")

    def load_image(self, input_path):
        """Wczytuje obraz z podanej ścieżki."""
        image = cv2.imread(input_path)
        if image is None:
            raise FileNotFoundError(f"Obraz nie został znaleziony pod ścieżką {input_path}")
        return image

    def process_fragment(self, fragment):
        """Przetwarza fragment obrazu, konwertując go na skalę szarości z użyciem szyfrowania homomorficznego."""
        fragment_height, fragment_width, _ = fragment.shape
        gray_fragment = np.zeros((fragment_height, fragment_width), dtype=np.float64)

        for i, color in enumerate(["B", "G", "R"]):
            channel = fragment[:, :, i].flatten().astype(np.float64)
            encoded_channel = self.HE.encodeFrac(channel)
            ctxt_channel = self.HE.encryptPtxt(encoded_channel)
            weight = self.weights[color]
            encoded_weight = self.HE.encodeFrac(np.full(self.HE.get_nSlots(), weight, dtype=np.float64))
            weighted_ctxt = ctxt_channel * encoded_weight
            decrypted_weighted = self.HE.decryptFrac(weighted_ctxt)
            gray_fragment += decrypted_weighted[:fragment_height * fragment_width].reshape((fragment_height, fragment_width))

        gray_fragment = np.clip(gray_fragment, 0, 255).astype(np.uint8)
        return gray_fragment

    def save_image(self, image, output_path):
        """Zapisuje przetworzony obraz w podanej ścieżce."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        print(f'Obraz w skali szarości zapisany pod {output_path}')

    def encrypt_and_convert(self, input_path, output_path):
        """Główna funkcja przetwarzająca cały obraz."""
        image = self.load_image(input_path)
        height, width, _ = image.shape
        fragment_size = 64

        self.initialize_context()
        gray_image = np.zeros((height, width), dtype=np.uint8)

        for y in range(0, height, fragment_size):
            for x in range(0, width, fragment_size):
                fragment = image[y:y+fragment_size, x:x+fragment_size]
                fragment_height, fragment_width, _ = fragment.shape

                if fragment_height == 0 or fragment_width == 0:
                    continue

                gray_fragment = self.process_fragment(fragment)
                gray_image[y:y+fragment_height, x:x+fragment_width] = gray_fragment

        self.save_image(gray_image, output_path)
        return output_path