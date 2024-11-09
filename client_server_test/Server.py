import socket
import sys
from Encryption import EncryptionHandler
from Pyfhel import PyCtxt

class Server:
    def __init__(self, host: str, port: int, scheme: str):
        self.host = host
        self.port = port
        self.encryption_handler = EncryptionHandler(scheme)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"Serwer nasłuchuje na {self.host}:{self.port} z użyciem schematu {scheme}.")
        except Exception as e:
            raise ConnectionError(f"Nie udało się uruchomić serwera: {e}")

    def send_data(self, client_socket, data: bytes):
        data_length = len(data)
        client_socket.sendall(data_length.to_bytes(4, byteorder='big'))
        client_socket.sendall(data)

    def receive_data(self, client_socket) -> bytes:
        try:
            data_length_bytes = client_socket.recv(4)
            if not data_length_bytes:
                return None
            data_length = int.from_bytes(data_length_bytes, byteorder='big')
            data = b''
            while len(data) < data_length:
                packet = client_socket.recv(data_length - len(data))
                if not packet:
                    return None
                data += packet
            return data
        except Exception as e:
            raise ConnectionError(f"Błąd podczas odbierania danych: {e}")

    def handle_client(self, client_socket):
        try:
            # Wysłanie klucza publicznego do klienta
            public_key_bytes = self.encryption_handler.serialize_public_key()
            self.send_data(client_socket, public_key_bytes)
            print("Klucz publiczny wysłano do klienta.")

            # Odbieranie zaszyfrowanej liczby od klienta
            data = self.receive_data(client_socket)
            if data is None:
                print("Serwer: Nie udało się odebrać danych od klienta.")
                return
            
            # Deserializacja zaszyfrowanej liczby
            ciphertext = PyCtxt(pyfhel=self.encryption_handler.HE, bytestring=data)
            print(f"Serwer otrzymał zaszyfrowane dane: {ciphertext}")

            # Wykonanie operacji na zaszyfrowanych danych (mnożenie przez 2)
            result_ciphertext = ciphertext + ciphertext
            print("Serwer wykonał operację mnożenia przez 2 na zaszyfrowanych danych.")

            # Serializacja zaszyfrowanego wyniku do wysłania
            result_data = result_ciphertext.to_bytes()
            self.send_data(client_socket, result_data)
            print("Serwer wysłał zaszyfrowany wynik do klienta.")
        except Exception as e:
            print(f"Błąd podczas obsługi klienta: {e}")

    def start(self):
        try:
            while True:
                client_socket, addr = self.socket.accept()
                print(f"Połączono z {addr}.")
                self.handle_client(client_socket)
                client_socket.close()
        except KeyboardInterrupt:
            print("Zamykanie serwera.")
        finally:
            self.socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Użycie: python server.py <host> <port> <schemat_szyfrowania>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    scheme = sys.argv[3]

    server = Server(host, port, scheme)
    server.start()
