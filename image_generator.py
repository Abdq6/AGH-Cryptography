import numpy as np
from PIL import Image
import os

class ImageGenerator:
    """
    A class for generating random images with distinct colors.
    """

    def __init__(self, output_folder='./input'):
        """
        Initializes the image generator and ensures the output folder exists.

        Parameters:
        output_folder (str): The folder where the generated images will be saved.
        """
        self.output_folder = os.path.abspath(output_folder)
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_random_image(self, width, height, output_filename):
        """
        Generates a random image with distinct colors and saves it to the output folder.

        Parameters:
        width (int): The width of the image.
        height (int): The height of the image.
        output_filename (str): The name of the output image file.

        Returns:
        str: The path to the saved image.
        """
        if os.path.dirname(output_filename):  # Ensure only the filename is used
            output_filename = os.path.basename(output_filename)

        distinct_colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
            (128, 0, 0),    # Maroon
            (0, 128, 0),    # Dark Green
            (0, 0, 128),    # Navy
            (128, 128, 0),  # Olive
            (0, 128, 128),  # Teal
            (128, 0, 128),  # Purple
            (192, 192, 192),# Silver
            (128, 128, 128),# Gray
            (0, 0, 0),      # Black
            (255, 255, 255) # White
        ]

        pixels = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixels[y, x] = distinct_colors[np.random.randint(len(distinct_colors))]

        image = Image.fromarray(pixels, 'RGB')
        output_path = os.path.join(self.output_folder, output_filename)
        image.save(output_path, 'JPEG')
        print(f'Image saved at {output_path}')
        return output_path
