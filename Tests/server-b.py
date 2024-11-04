import socket
import struct
from Pyfhel import Pyfhel, PyCtxt
import pickle
import numpy as np

HOST = '0.0.0.0'
PORT = 5000

# Inicjalizacja Pyfhel i import klucza publicznego
HE = Pyfhel()
HE.contextGen(p=65537, m=8192, sec=128)
with open("public_key.pkl", "rb") as pk_file:
    HE.from_bytes_publicKey(pk_file.read())

def process_encrypted_image(conn):
    data_size = struct.unpack('!I', conn.recv(4))[0]
    encrypted_data = conn.recv(data_size)
    encrypted_data = pickle.loads(encrypted_data)

    processed_data = []
    for encrypted_row in encrypted_data:
        processed_row = []
        for enc_r, enc_g, enc_b in encrypted_row:
            # Konwersja na odcienie szarości na zaszyfrowanych danych
            enc_gray = HE.multiplyFrac(enc_r, 0.299) + HE.multiplyFrac(enc_g, 0.587) + HE.multiplyFrac(enc_b, 0.114)
            processed_row.append(enc_gray)
        processed_data.append(processed_row)

    serialized_result = pickle.dumps(processed_data)
    conn.sendall(struct.pack('!I', len(serialized_result)))
    conn.sendall(serialized_result)
    print("Zaszyfrowane odcienie szarości obrazu zostały wysłane")

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer nasłuchuje na {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Połączono z {addr}")
            process_encrypted_image(conn)
