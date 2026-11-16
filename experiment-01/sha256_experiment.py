
import hashlib

def sha256(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def bit_difference(hash1, hash2):
    a = int(hash1, 16)
    b = int(hash2, 16)
    return bin(a ^ b).count("1")

# Experiment inputs
messages = [
    "Bitcoin",
    "bitcoin",
    "Bitcoin ",
    "Bitcoin"
]

print("=" * 55)
print("BITCOIN SHA-256 RESEARCH EXPERIMENT")
print("=" * 55)

results = []

for message in messages:
    result = sha256(message)
    results.append(result)

    print("\nInput:", repr(message))
    print("SHA-256:", result)
    print("Hash length:", len(result))
    print("Output bits:", len(result) * 4)

# Deterministic property
print("\n--- DETERMINISTIC TEST ---")
print("Same input, same hash:",
      results[0] == results[3])

# Avalanche effect
print("\n--- AVALANCHE EFFECT ---")

difference = bit_difference(results[0], results[1])

print("Original input: Bitcoin")
print("Modified input: bitcoin")
print("Changed output bits:", difference)
print("Percentage changed:",
      round(difference / 256 * 100, 2), "%")

# Double SHA-256
print("\n--- DOUBLE SHA-256 TEST ---")

first_hash = hashlib.sha256(
    b"Bitcoin"
).digest()

double_hash = hashlib.sha256(
    first_hash
).hexdigest()

print("Single SHA-256:", results[0])
print("Double SHA-256:", double_hash)

print("\nEXPERIMENT COMPLETED")
