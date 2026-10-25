import hashlib

with open("record.txt", "rb") as f:
    data = f.read()

hash_val = hashlib.sha256(data).hexdigest()

print("Hash:", hash_val)
