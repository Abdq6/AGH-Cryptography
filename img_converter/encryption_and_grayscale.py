import numpy as np
from Pyfhel import Pyfhel
import cv2
import os

class EncryptionAndGrayscale:
    def __init__(self):
        self.HE = None
        self.context_initialized = False
        self.current_encryption_method = None
        self.slot_size = 2**13
        self.scale = 2**40
        self.qi_sizes_ckks = [60, 40, 40, 60]
        self.qi_sizes_bfv_bgv = [60, 30, 30, 60]
        self.plain_modulus = 65537  # Moduł plaintext t
        self.weights_float = {"B": 0.1140, "G": 0.5870, "R": 0.2989}
        self.weights_int = {"B": 29, "G": 150, "R": 76}  # Wagi całkowite

    def initialize_context(self, encryption_method):
        """Inicjalizuje kontekst Pyfhel dla wybranego schematu szyfrowania."""
        if not self.context_initialized or self.current_encryption_method != encryption_method:
            self.HE = Pyfhel()
            if encryption_method == "CKKS":
                self.HE.contextGen(
                    scheme="CKKS",
                    n=self.slot_size * 2,  # CKKS wymaga większego n
                    scale=self.scale,
                    qi_sizes=self.qi_sizes_ckks
                )
                self.HE.keyGen()
                print(f"Kontekst CKKS zainicjowany z n={self.slot_size * 2}, scale={self.scale}, qi_sizes={self.qi_sizes_ckks}")
            elif encryption_method == "BFV":
                self.HE.contextGen(
                    scheme="BFV",
                    n=self.slot_size,
                    t=self.plain_modulus,
                    qi_sizes=self.qi_sizes_bfv_bgv
                )
                self.HE.keyGen()
                print(f"Kontekst BFV zainicjowany z n={self.slot_size}, t={self.plain_modulus}, qi_sizes={self.qi_sizes_bfv_bgv}")
            elif encryption_method == "BGV":
                self.HE.contextGen(
                    scheme="BGV",
                    n=self.slot_size,
                    t=self.plain_modulus,
                    qi_sizes=self.qi_sizes_bfv_bgv
                )
                self.HE.keyGen()
                print(f"Kontekst BGV zainicjowany z n={self.slot_size}, t={self.plain_modulus}, qi_sizes={self.qi_sizes_bfv_bgv}")
            else:
                raise ValueError(f"Nieznana metoda szyfrowania: {encryption_method}")
            self.context_initialized = True
            self.current_encryption_method = encryption_method

    def load_image(self, input_path):
        """Wczytuje obraz z podanej ścieżki."""
        image = cv2.imread(input_path)
        if image is None:
            raise FileNotFoundError(f"Obraz nie został znaleziony pod ścieżką {input_path}")
        return image

    def process_fragment(self, fragment, encryption_method):
        """Przetwarza fragment obrazu, konwertując go na skalę szarości."""
        fragment_height, fragment_width, _ = fragment.shape

        if encryption_method == "CKKS":
            gray_fragment = np.zeros((fragment_height, fragment_width), dtype=np.float64)
            for i, color in enumerate(["B", "G", "R"]):
                channel = fragment[:, :, i].flatten().astype(np.float64)
                encoded_channel = self.HE.encodeFrac(channel)
                ctxt_channel = self.HE.encryptPtxt(encoded_channel)
                weight = self.weights_float[color]
                encoded_weight = self.HE.encodeFrac(np.full(len(channel), weight, dtype=np.float64))
                weighted_ctxt = ctxt_channel * encoded_weight
                decrypted_weighted = self.HE.decryptFrac(weighted_ctxt)
                decrypted_weighted = decrypted_weighted[:fragment_height * fragment_width]
                gray_fragment += decrypted_weighted.reshape((fragment_height, fragment_width))
            gray_fragment = np.clip(gray_fragment, 0, 255).astype(np.uint8)

        elif encryption_method in ["BFV", "BGV"]:
            gray_fragment = np.zeros((fragment_height, fragment_width), dtype=np.uint8)
            num_slots = self.HE.get_nSlots()
            channels = {}

            for i, color in enumerate(["B", "G", "R"]):
                channel = fragment[:, :, i].flatten().astype(np.int64)
                padded_channel = np.pad(channel, (0, num_slots - len(channel)), 'constant')[:num_slots]
                channels[color] = padded_channel

            ctxt_channels = {}
            for color in ["B", "G", "R"]:
                encoded_channel = self.HE.encodeInt(channels[color])
                ctxt_channel = self.HE.encrypt(encoded_channel)
                ctxt_channels[color] = ctxt_channel

            ctxt_gray = ctxt_channels["B"] * self.weights_int["B"]
            ctxt_gray += ctxt_channels["G"] * self.weights_int["G"]
            ctxt_gray += ctxt_channels["R"] * self.weights_int["R"]

            decrypted_gray = self.HE.decrypt(ctxt_gray)
            decrypted_gray = np.array(decrypted_gray[:fragment_height * fragment_width], dtype=np.int64)
            gray_fragment = (decrypted_gray // 255).reshape((fragment_height, fragment_width))
            gray_fragment = np.clip(gray_fragment, 0, 255).astype(np.uint8)
        else:
            raise ValueError(f"Nieznana metoda szyfrowania: {encryption_method}")

        return gray_fragment

    def save_image(self, image, output_path):
        """Zapisuje przetworzony obraz w podanej ścieżce."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        print(f'Obraz w skali szarości zapisany pod {output_path}')

    def encrypt_and_convert(self, input_path, output_path, encryption_method="CKKS"):
        """Główna funkcja przetwarzająca cały obraz."""
        image = self.load_image(input_path)
        height, width, _ = image.shape
        fragment_size = 64

        self.initialize_context(encryption_method)
        gray_image = np.zeros((height, width), dtype=np.uint8)

        for y in range(0, height, fragment_size):
            for x in range(0, width, fragment_size):
                fragment = image[y:y+fragment_size, x:x+fragment_size]
                fragment_height, fragment_width, _ = fragment.shape
                if fragment_height == 0 or fragment_width == 0:
                    continue
                gray_fragment = self.process_fragment(fragment, encryption_method)
                gray_image[y:y+fragment_height, x:x+fragment_width] = gray_fragment

        self.save_image(gray_image, output_path)
        return output_path
