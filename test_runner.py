import os
import time
import csv
from image_generator import ImageGenerator
from encryption_and_grayscale import EncryptionAndGrayscale

class TestRunner:
    """
    Class for running tests on image encryption and grayscale conversion methods.
    """

    def __init__(self):
        """
        Initializes the test runner with an image generator and creates necessary directories.
        """
        self.image_generator = ImageGenerator()
        self.input_folder = './input'
        self.output_folder = './output'
        self.csv_folder = './csv'
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.csv_folder, exist_ok=True)

    def run_tests(self, image_sizes, encryption_methods):
        """
        Runs tests for different image sizes and encryption methods.

        Parameters:
        image_sizes (list of tuple): List of (width, height) pairs for images to test.
        encryption_methods (list of str): List of encryption methods ("CKKS", "BFV", "BGV").

        Saves:
        The results are saved as a CSV file in the csv folder.
        """
        results = []
        for method in encryption_methods:
            encryption_and_grayscale = EncryptionAndGrayscale()
            for width, height in image_sizes:
                image_filename = f'random_image_{width}x{height}.jpg'
                image_path = os.path.join(self.input_folder, image_filename)
                self.image_generator.generate_random_image(width, height, image_path)
                gray_image_filename = f'grayscale_{method}_{width}x{height}.jpg'
                gray_image_path = os.path.join(self.output_folder, gray_image_filename)
                start_time = time.time()
                try:
                    encryption_and_grayscale.encrypt_and_convert(
                        input_path=image_path,
                        output_path=gray_image_path,
                        encryption_method=method
                    )
                    success = True
                except Exception as e:
                    print(f'Error processing method {method} for image {width}x{height}: {e}')
                    success = False
                conversion_time = time.time() - start_time
                results.append([method, width, height, conversion_time, success])
        self.save_results(results)

    def save_results(self, results):
        """
        Saves the test results to a CSV file.

        Parameters:
        results (list of list): List of results, where each result is a list with
                                [method, width, height, time, success].
        """
        results_path = os.path.join(self.csv_folder, 'conversion_times.csv')
        with open(results_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Method', 'Width', 'Height', 'Time (s)', 'Success'])
            writer.writerows(results)
        print(f'Results saved to {results_path}')


if __name__ == '__main__':
    image_sizes = [(100, 100), (500, 500)]
    encryption_methods = ['CKKS', 'BFV', 'BGV']
    test_runner = TestRunner()
    test_runner.run_tests(image_sizes, encryption_methods)
