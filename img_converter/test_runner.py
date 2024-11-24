import os
import time
import csv
from image_generator import ImageGenerator
from encryption_and_grayscale import EncryptionAndGrayscale

class TestRunner:
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.results_folder = './results'
        os.makedirs(self.results_folder, exist_ok=True)

    def run_tests(self, image_sizes, encryption_methods):
        results = []
        for method in encryption_methods:
            encryption_and_grayscale = EncryptionAndGrayscale()
            for width, height in image_sizes:
                image_filename = f'random_image_{width}x{height}.jpg'
                image_path = self.image_generator.generate_random_image(width, height, image_filename)

                start_time = time.time()
                gray_image_path = f'./img/grayscale_{method}_{width}x{height}.jpg'
                try:
                    encryption_and_grayscale.encrypt_and_convert(image_path, gray_image_path, encryption_method=method)
                    success = True
                except Exception as e:
                    print(f'Błąd podczas przetwarzania metodą {method} dla obrazu {width}x{height}: {e}')
                    success = False
                conversion_time = time.time() - start_time

                results.append([method, width, height, conversion_time, success])

        self.save_results(results)

    def save_results(self, results):
        results_path = os.path.join(self.results_folder, 'conversion_times.csv')
        with open(results_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Metoda', 'Szerokość', 'Wysokość', 'Czas (s)', 'Sukces'])
            writer.writerows(results)
        print(f'Rezultaty zapisane w {results_path}')


# Główna funkcja
if __name__ == '__main__':
    image_sizes = [(100, 100), (500, 500)]
    encryption_methods = ['CKKS', 'BFV', 'BGV']
    test_runner = TestRunner()
    test_runner.run_tests(image_sizes, encryption_methods)
