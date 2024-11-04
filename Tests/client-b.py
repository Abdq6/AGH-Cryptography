import socket
import struct
from Pyfhel import Pyfhel, PyCtxt
import numpy as np
from PIL import Image
import pickle

HOST = '127.0.0.1'
PORT = 5000

# Inicjalizacja Pyfhel
HE = Pyfhel()
HE.contextGen(p=65537, m=8192, sec=128)  # Parametry mogą być dostosowane do potrzeb
HE.keyGen()

# Eksport klucza publicznego, aby serwer mógł go używać
public_key = HE.to_bytes_publicKey()
with open("public_key.pkl", "wb") as pk_file:
    pk_file.write(public_key)

def encrypt_and_send_image(s, filename):
    image = Image.open(filename)
    image_data = np.array(image)

    encrypted_data = []
    for row in image_data:
        encrypted_row = []
        for pixel in row:
            r, g, b = pixel
            enc_r = HE.encryptFrac(float(r))
            enc_g = HE.encryptFrac(float(g))
            enc_b = HE.encryptFrac(float(b))
            encrypted_row.append((enc_r, enc_g, enc_b))
        encrypted_data.append(encrypted_row)

    serialized_data = pickle.dumps(encrypted_data)
    s.sendall(struct.pack('!I', len(serialized_data)))
    s.sendall(serialized_data)
    print(f"Zaszyfrowany obraz '{filename}' został wysłany")

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        encrypt_and_send_image(s, 'Input/small_image.jpg')
