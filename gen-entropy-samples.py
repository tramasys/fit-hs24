import os
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

NUM_FILES = 1000
FILE_SIZE = 100000

def generate_text(entropy, length):
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
    charset = charset[:int(2 ** entropy)]
    return ''.join(random.choice(charset) for _ in range(length))


def create_files(directory, num_files, file_size):
    os.makedirs(directory, exist_ok=True)

    # Generate entropy values from 1 to 8 in equal steps based on the number of files
    entropies = [1 + i * 7 / (num_files - 1) for i in range(num_files)]

    for i, entropy in enumerate(entropies):
        filename = f"file_{i:03d}_entropy.txt"
        content = generate_text(entropy, file_size)

        with open(os.path.join(directory, filename), "w") as file:
            file.write(content)

        print(f"Created {filename}")


# Create 100 files, each with 100,000 characters
create_files("samples/entropy", NUM_FILES, FILE_SIZE)




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


# encrypt every 10th file
for i in range(0, NUM_FILES, 10):
    input_filename = f"samples/entropy/file_{i:03d}_entropy.txt"
    encrypted_filename = f"samples/entropy/encrypted_file_{i:03d}_entropy.txt"
    key = get_random_bytes(32)
    encrypt_file(input_filename, encrypted_filename, key)

    print(f"Encrypted {input_filename} to {encrypted_filename}")