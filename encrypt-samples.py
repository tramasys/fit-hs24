import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

os.makedirs("samples/entropy", exist_ok=True)

def encrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        data = f.read()

    initialization_vector = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)

    padding_length = 16 - len(data) % 16
    padded_data = data + bytes([padding_length]) * padding_length

    ciphertext = cipher.encrypt(padded_data)

    with open(output_file, "wb") as f:
        f.write(initialization_vector + ciphertext)


key = get_random_bytes(32)

input_filename = "samples/performance/random.txt"
encrypted_filename = "samples/entropy/encrypted_random.txt"
encrypt_file(input_filename, encrypted_filename, key)