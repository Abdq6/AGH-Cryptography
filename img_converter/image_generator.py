import numpy as np
from PIL import Image
import os

class ImageGenerator:
    def __init__(self, output_folder='./img'):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def generate_random_image(self, width, height, output_filename):
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
        
        # Create an empty image with random colors
        pixels = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixels[y, x] = distinct_colors[np.random.randint(len(distinct_colors))]

        # Convert numpy array to image
        image = Image.fromarray(pixels, 'RGB')

        # Save the image
        output_path = os.path.join(self.output_folder, output_filename)
        image.save(output_path, 'JPEG')
        print(f'Image saved at {output_path}')
        return output_path
