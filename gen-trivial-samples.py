import os
import random
import string

os.makedirs("samples/performance", exist_ok=True)

samples = {
    "a.txt": "a",
    "aaa.txt": "a" * 100000,
    "alphabet.txt": (string.ascii_lowercase * (100000 // 26 + 1))[:100000],
    "random.txt": "".join(
        random.choices(string.ascii_letters + string.digits, k=100000)
    ),
}

for filename, content in samples.items():
    with open(os.path.join("samples/performance", filename), "w") as file:
        file.write(content)
