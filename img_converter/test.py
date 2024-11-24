import os
from encryption_and_grayscale import EncryptionAndGrayscale

def process_image_all_methods(input_path):
    """Przetwarza obraz wszystkimi metodami szyfrowania."""
    output_folder = '/home/parallels/projekty/AGH-Cryptography/Tests/Output/'
    os.makedirs(output_folder, exist_ok=True)

    encryption_methods = ['CKKS', 'BFV', 'BGV']
    results = []

    for method in encryption_methods:
        output_path = os.path.join(output_folder, f'small_image_{method}.jpg')
        encryption_and_grayscale = EncryptionAndGrayscale()
        try:
            encryption_and_grayscale.encrypt_and_convert(input_path, output_path, encryption_method=method)
            print(f"Przetwarzanie zakończone dla metody {method}. Wynik zapisano w {output_path}")
            results.append((method, "Sukces"))
        except Exception as e:
            print(f"Błąd podczas przetwarzania metodą {method}: {e}")
            results.append((method, f"Błąd: {e}"))

    return results


if __name__ == "__main__":
    input_path = "/home/parallels/projekty/AGH-Cryptography/Tests/Input/small_image.jpg"
    results = process_image_all_methods(input_path)

    print("\nPodsumowanie:")
    for method, status in results:
        print(f"Metoda: {method}, Status: {status}")
