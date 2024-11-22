import os
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

os.makedirs("samples", exist_ok=True)

samples = {
    "a.txt": "a",
    "aaa.txt": "a" * 100000,
    "alphabet.txt": (string.ascii_lowercase * (100000 // 26 + 1))[:100000],
    "random.txt": "".join(
        random.choices(string.ascii_letters + string.digits, k=100000)
    ),
}

for filename, content in samples.items():
    with open(os.path.join("samples", filename), "w") as file:
        file.write(content)


def encrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        data = f.read()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    padding_length = 16 - len(data) % 16
    padded_data = data + bytes([padding_length]) * padding_length

    ciphertext = cipher.encrypt(padded_data)

    with open(output_file, "wb") as f:
        f.write(iv + ciphertext)


key = get_random_bytes(32)

input_filename = "samples/random.txt"
encrypted_filename = "samples/encrypted_random.txt"
encrypt_file(input_filename, encrypted_filename, key)
