import time
import os
import csv
from image_generator import ImageGenerator
from encryption_and_grayscale import EncryptionAndGrayscale

class TestRunner:
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.encryption_and_grayscale = EncryptionAndGrayscale()
        self.results_folder = './results'
        os.makedirs(self.results_folder, exist_ok=True)

    def run_tests(self, image_sizes):
        results = []
        for width, height in image_sizes:
            # Generate image
            image_filename = f'random_image_{width}x{height}.jpg'
            image_path = self.image_generator.generate_random_image(width, height, image_filename)
            
            # Measure the time taken for encryption and grayscale conversion
            start_time = time.time()
            gray_image_path = f'./img/grayscale_{width}x{height}.jpg'
            self.encryption_and_grayscale.encrypt_and_convert(image_path, gray_image_path)
            conversion_time = time.time() - start_time
            
            # Store the results
            results.append([width, height, conversion_time])

        # Save results to CSV
        self.save_results(results)

    def save_results(self, results):
        results_path = os.path.join(self.results_folder, 'conversion_times.csv')
        with open(results_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Width', 'Height', 'Conversion Time (seconds)'])
            writer.writerows(results)
        print(f'Results saved to {results_path}')


# Run the tests
if __name__ == '__main__':
    image_sizes = [(100, 100), (500, 500), (1000, 1000), (2500, 2500)]
    test_runner = TestRunner()
    test_runner.run_tests(image_sizes)
