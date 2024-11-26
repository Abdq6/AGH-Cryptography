import numpy as np
from Pyfhel import Pyfhel
import cv2
import os

class EncryptionAndGrayscale:
    """
    A class for encrypting images and converting them to grayscale using homomorphic encryption.
    """

    def __init__(self):
        """
        Initializes the class with default encryption parameters and grayscale weights.
        """
        self.HE = None
        self.context_initialized = False
        self.current_encryption_method = None
        self.slot_size = 2**13
        self.scale = 2**40
        self.qi_sizes_ckks = [60, 40, 40, 60]
        self.qi_sizes_bfv_bgv = [60, 30, 30, 60]
        self.plain_modulus = 65537
        self.weights_float = {"B": 0.1140, "G": 0.5870, "R": 0.2989}
        self.weights_int = {"B": int(0.1140 * 255), "G": int(0.5870 * 255), "R": int(0.2989 * 255)}

    def initialize_context(self, encryption_method):
        """
        Initializes the Pyfhel encryption context for the specified method.

        Parameters:
        encryption_method (str): The encryption scheme to use ("CKKS", "BFV", or "BGV").
        
        Raises:
        ValueError: If an unknown encryption method is provided.
        """
        if self.context_initialized and self.current_encryption_method == encryption_method:
            return

        self.HE = Pyfhel()
        if encryption_method == "CKKS":
            self._initialize_ckks()
        elif encryption_method == "BFV":
            self._initialize_bfv()
        elif encryption_method == "BGV":
            self._initialize_bgv()
        else:
            raise ValueError(f"Unknown encryption method: {encryption_method}")

        self.context_initialized = True
        self.current_encryption_method = encryption_method

    def _initialize_ckks(self):
        """
        Initializes the CKKS encryption context.
        """
        self.HE.contextGen(
            scheme="CKKS",
            n=self.slot_size * 2,
            scale=self.scale,
            qi_sizes=self.qi_sizes_ckks
        )
        self.HE.keyGen()
        print(f"CKKS context initialized with n={self.slot_size * 2}, scale={self.scale}, qi_sizes={self.qi_sizes_ckks}")

    def _initialize_bfv(self):
        """
        Initializes the BFV encryption context.
        """
        self.HE.contextGen(
            scheme="BFV",
            n=self.slot_size,
            t=self.plain_modulus,
            qi_sizes=self.qi_sizes_bfv_bgv
        )
        self.HE.keyGen()
        print(f"BFV context initialized with n={self.slot_size}, t={self.plain_modulus}, qi_sizes={self.qi_sizes_bfv_bgv}")

    def _initialize_bgv(self):
        """
        Initializes the BGV encryption context.
        """
        self.HE.contextGen(
            scheme="BGV",
            n=self.slot_size,
            t=self.plain_modulus,
            qi_sizes=self.qi_sizes_bfv_bgv
        )
        self.HE.keyGen()
        print(f"BGV context initialized with n={self.slot_size}, t={self.plain_modulus}, qi_sizes={self.qi_sizes_bfv_bgv}")

    def load_image(self, input_path):
        """
        Loads an image from the specified file path.

        Parameters:
        input_path (str): The file path of the image to load.

        Returns:
        np.ndarray: The loaded image.

        Raises:
        FileNotFoundError: If the image is not found at the specified path.
        """
        image = cv2.imread(input_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {input_path}")
        return image

    def _prepare_channels(self, fragment, num_slots):
        """
        Prepares the image channels for encryption by padding and encoding them.

        Parameters:
        fragment (np.ndarray): The image fragment to process.
        num_slots (int): The number of slots in the encryption scheme.

        Returns:
        dict: A dictionary containing encrypted channels for "B", "G", and "R".
        """
        channels = {}
        for i, color in enumerate(["B", "G", "R"]):
            channel = fragment[:, :, i].flatten().astype(np.int64)
            padded_channel = np.pad(channel, (0, num_slots - len(channel)), 'constant')[:num_slots]
            encoded_channel = self.HE.encodeInt(padded_channel)
            channels[color] = self.HE.encrypt(encoded_channel)
        return channels

    def _combine_channels_bfv_bgv(self, channels):
        """
        Combines encrypted channels using the weights to create a grayscale encrypted image.

        Parameters:
        channels (dict): A dictionary containing encrypted channels for "B", "G", and "R".

        Returns:
        Pyfhel.Ciphertext: The encrypted grayscale representation.
        """
        return (
            channels["B"] * self.weights_int["B"] +
            channels["G"] * self.weights_int["G"] +
            channels["R"] * self.weights_int["R"]
        )

    def process_fragment(self, fragment, encryption_method):
        """
        Processes an image fragment, converting it to grayscale using the specified encryption method.

        Parameters:
        fragment (np.ndarray): The image fragment to process.
        encryption_method (str): The encryption scheme to use ("CKKS", "BFV", or "BGV").

        Returns:
        np.ndarray: The processed grayscale fragment.

        Raises:
        ValueError: If an unknown encryption method is provided.
        """
        if encryption_method == "CKKS":
            return self._process_ckks_fragment(fragment)
        elif encryption_method in ["BFV", "BGV"]:
            return self._process_bfv_bgv_fragment(fragment)
        else:
            raise ValueError(f"Unknown encryption method: {encryption_method}")

    def _process_ckks_fragment(self, fragment):
        """
        Converts an image fragment to grayscale using the CKKS encryption method.

        Parameters:
        fragment (np.ndarray): The image fragment to process.

        Returns:
        np.ndarray: The grayscale fragment.
        """
        fragment_height, fragment_width, _ = fragment.shape
        gray_fragment = np.zeros((fragment_height, fragment_width), dtype=np.float64)

        for i, color in enumerate(["B", "G", "R"]):
            channel = fragment[:, :, i].flatten().astype(np.float64)
            gray_fragment += self._encrypt_and_decrypt_ckks(channel, self.weights_float[color], fragment_height, fragment_width)

        return np.clip(gray_fragment, 0, 255).astype(np.uint8)

    def _encrypt_and_decrypt_ckks(self, channel, weight, height, width):
        """
        Encrypts and decrypts a single channel using CKKS.

        Parameters:
        channel (np.ndarray): The image channel to encrypt and decrypt.
        weight (float): The weight for the channel in the grayscale conversion.
        height (int): The height of the fragment.
        width (int): The width of the fragment.

        Returns:
        np.ndarray: The decrypted and weighted channel as part of the grayscale conversion.
        """
        encoded_channel = self.HE.encodeFrac(channel)
        ctxt_channel = self.HE.encryptPtxt(encoded_channel)
        weighted_ctxt = ctxt_channel * weight
        decrypted_weighted = self.HE.decryptFrac(weighted_ctxt)
        return decrypted_weighted[:height * width].reshape((height, width))

    def _process_bfv_bgv_fragment(self, fragment):
        """
        Converts an image fragment to grayscale using BFV or BGV encryption methods.

        Parameters:
        fragment (np.ndarray): The image fragment to process.

        Returns:
        np.ndarray: The grayscale fragment.
        """
        fragment_height, fragment_width, _ = fragment.shape
        gray_fragment = np.zeros((fragment_height, fragment_width), dtype=np.uint8)
        num_slots = self.HE.get_nSlots()

        channels = self._prepare_channels(fragment, num_slots)
        ctxt_gray = self._combine_channels_bfv_bgv(channels)
        decrypted_gray = self._decrypt_and_normalize(ctxt_gray, fragment_height, fragment_width)

        return np.clip(decrypted_gray, 0, 255).astype(np.uint8)

    def _decrypt_and_normalize(self, ctxt_gray, height, width):
        """
        Decrypts and normalizes the grayscale encrypted image fragment.

        Parameters:
        ctxt_gray (Pyfhel.Ciphertext): The encrypted grayscale fragment.
        height (int): The height of the fragment.
        width (int): The width of the fragment.

        Returns:
        np.ndarray: The normalized grayscale fragment.
        """
        decrypted_gray = self.HE.decrypt(ctxt_gray)
        decrypted_gray = np.array(decrypted_gray[:height * width], dtype=np.int64)
        decrypted_gray -= decrypted_gray.min()  # Shift to zero
        return (decrypted_gray / decrypted_gray.max() * 255).reshape((height, width))

    def save_image(self, image, output_path):
        """
        Saves an image to the specified file path.

        Parameters:
        image (np.ndarray): The image to save.
        output_path (str): The file path to save the image.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        print(f'Grayscale image saved to {output_path}')

    def encrypt_and_convert(self, input_path, output_path, encryption_method="CKKS"):
        """
        Main function to process an image: encrypt it and convert it to grayscale.

        Parameters:
        input_path (str): The file path of the input image.
        output_path (str): The file path for the processed output image.
        encryption_method (str): The encryption method to use ("CKKS", "BFV", "BGV").

        Returns:
        str: The path of the saved grayscale image.
        """
        image = self.load_image(input_path)
        self.initialize_context(encryption_method)

        height, width, _ = image.shape
        gray_image = self._process_image_fragments(image, height, width, encryption_method)
        self.save_image(gray_image, output_path)
        return output_path

    def _process_image_fragments(self, image, height, width, encryption_method, fragment_size=64):
        """
        Processes the image in fragments, converting each fragment to grayscale.

        Parameters:
        image (np.ndarray): The full image to process.
        height (int): The height of the image.
        width (int): The width of the image.
        encryption_method (str): The encryption method to use ("CKKS", "BFV", "BGV").
        fragment_size (int, optional): The size of each fragment (default: 64).

        Returns:
        np.ndarray: The full grayscale image.
        """
        gray_image = np.zeros((height, width), dtype=np.uint8)

        for y in range(0, height, fragment_size):
            for x in range(0, width, fragment_size):
                fragment = image[y:y+fragment_size, x:x+fragment_size]
                if fragment.size == 0:
                    continue

                try:
                    gray_fragment = self.process_fragment(fragment, encryption_method)
                    gray_image[y:y+fragment.shape[0], x:x+fragment.shape[1]] = gray_fragment
                except Exception as e:
                    print(f"Error processing fragment at ({x}, {y}): {e}")
                    raise e

        return gray_image
