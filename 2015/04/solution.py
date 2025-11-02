import hashlib
import itertools

secret_key = "bgvyzdsv"

# Part 1
for i in itertools.count():
    hash = hashlib.md5((secret_key + str(i)).encode()).hexdigest()
    if hash.startswith("00000"):
        print(f"Number to produce hash: {i} (hash={hash})")
        break
