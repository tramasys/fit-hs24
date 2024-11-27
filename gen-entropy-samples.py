import os
import random

NUM_FILES = 100
FILE_SIZE = 100000


def generate_bytes(entropy, length):
    byte_range = bytes(range(256))
    max_byte_range = int(2 ** entropy)
    selected_bytes = byte_range[:max_byte_range]
    return bytes(random.choice(selected_bytes) for _ in range(length))


def create_files(directory, num_files, file_size):
    os.makedirs(directory, exist_ok=True)

    # Generate entropy values from 1 to 8 in equal steps based on the number of files
    entropies = [1 + i * 7 / (num_files - 1) for i in range(num_files)]

    for i, entropy in enumerate(entropies):
        filename = f"file_{i:03d}_entropy.txt"
        content = generate_bytes(entropy, file_size)

        with open(os.path.join(directory, filename), "wb") as file:
            file.write(content)

        print(f"Created {filename}")


create_files("samples/entropy", NUM_FILES, FILE_SIZE)
