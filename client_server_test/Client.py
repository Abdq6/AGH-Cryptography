import socket
import sys
from Encryption import EncryptionHandler

class Client:
    def __init__(self, host: str, port: int, scheme: str):
        self.host = host
        self.port = port
        self.encryption_handler = EncryptionHandler(scheme)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            raise ConnectionError(f"Nie udało się połączyć z serwerem: {e}")

    def send_data(self, data: bytes):
        data_length = len(data)
        self.socket.sendall(data_length.to_bytes(4, byteorder='big'))
        self.socket.sendall(data)

    def receive_data(self) -> bytes:
        try:
            data_length_bytes = self.socket.recv(4)
            if not data_length_bytes:
                raise ConnectionError("Nie udało się odebrać długości danych.")
            data_length = int.from_bytes(data_length_bytes, byteorder='big')
            data = b''
            while len(data) < data_length:
                packet = self.socket.recv(data_length - len(data))
                if not packet:
                    raise ConnectionError("Połączenie przerwane podczas odbierania danych.")
                data += packet
            return data
        except Exception as e:
            raise ConnectionError(f"Błąd podczas odbierania danych: {e}")

    def send_number(self, number: float):
        # Odbieranie klucza publicznego od serwera
        public_key_bytes = self.receive_data()
        self.encryption_handler.load_public_key(public_key_bytes)
        print("Klucz publiczny załadowano pomyślnie.")

        # Szyfrowanie liczby
        ciphertext_bytes = self.encryption_handler.encrypt(number)
        print(f"Zaszyfrowano liczbę: {number}")

        # Wysłanie zaszyfrowanej liczby do serwera
        self.send_data(ciphertext_bytes)
        print("Zaszyfrowana liczba została wysłana do serwera.")

        # Odbieranie zaszyfrowanego wyniku od serwera
        result_ciphertext_bytes = self.receive_data()
        print("Otrzymano zaszyfrowany wynik od serwera.")

        # Odszyfrowanie wyniku
        result = self.encryption_handler.decrypt(result_ciphertext_bytes)
        print(f"Otrzymany wynik: {result}")

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Użycie: python client.py <host> <port> <schemat_szyfrowania> <liczba>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    scheme = sys.argv[3]
    try:
        number = float(sys.argv[4])
    except ValueError:
        print("Podana liczba jest nieprawidłowa.")
        sys.exit(1)

    client = Client(host, port, scheme)
    try:
        client.send_number(number)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client.close()
