import socket
import struct
import time

HOST = '0.0.0.0'
PORT = 5000


def receive_file(conn, filename):
    data = conn.recv(4)
    if not data:
        return False
    file_size = struct.unpack('!I', data)[0]
    print(f"Odbieranie pliku '{filename}' o rozmiarze {file_size} bajtów")

    # odbieramy plik
    bytes_received = 0
    with open(filename, 'wb') as f:
        while bytes_received < file_size:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            bytes_received += len(data)
    print(f"Plik '{filename}' został odebrany")
    return True


def send_file(conn, filename):
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        # Wysyłanie rozmiaru pliku
        conn.sendall(struct.pack('!I', len(file_data)))
        # Wysyłanie danych pliku
        conn.sendall(file_data)
        print(f"Plik '{filename}' został wysłany")
    except FileNotFoundError:
        print(f"Plik '{filename}' nie istnieje")
        # Wysyłanie rozmiaru pliku 0, aby zasygnalizować brak pliku
        conn.sendall(struct.pack('!I', 0))

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer nasłuchuje na {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Połączono z {addr}")

            # Odbieranie pliku od klienta
            if receive_file(conn, 'received_image.jpg'):
                # obrobka pliku
                time.sleep(1)
                # Wysyłanie pliku z powrotem do klienta
                send_file(conn, 'received_image.jpg')