import socket
import struct
from numpy import asarray
HOST = '127.0.0.1'  # serwer obrabiajacy
PORT = 5000


def send_file(s, filename):
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        numpydata = asarray(file_data)
        s.sendall(struct.pack('!I', len(numpydata)))
        # Wysyłanie danych pliku tu będzie funkcja zwracająca zawszyfrowane file_data
        s.sendall(file_data)
        print(f"Plik '{filename}' został wysłany")
    except FileNotFoundError:
        print(f"Plik '{filename}' nie istnieje")
        s.sendall(struct.pack('!I', 0))


def receive_file(s, filename):
    # Odbieranie rozmiaru pliku
    data = s.recv(4)
    if not data:
        return False
    file_size = struct.unpack('!I', data)[0]
    if file_size == 0:
        print(f"Serwer nie przesłał pliku '{filename}'")
        return False

    print(f"Odbieranie pliku '{filename}' o rozmiarze {file_size} bajtów")

    # Odbieranie pliku
    bytes_received = 0
    with open(filename, 'wb') as f:
        while bytes_received < file_size:
            data = s.recv(1024)
            if not data:
                break
            #tu musimy odszyfrować data
            f.write(data)
            bytes_received += len(data)
    print(f"Plik '{filename}' został odebrany")
    return True


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Wysyłanie pliku do serwera
        send_file(s, 'Input/small_image.jpg')
        # Odbieranie pliku z serwera
        receive_file(s, 'Output/returned_image.jpg')
