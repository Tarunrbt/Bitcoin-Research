
import hashlib
import json

with open("mining_result.json") as f:
    result = json.load(f)

header = (
    f"{result['version']}|"
    f"{result['previous_hash']}|"
    f"{result['merkle_root']}|"
    f"{result['timestamp']}|"
    f"{result['nonce']}"
).encode("utf-8")

first_hash = hashlib.sha256(header).digest()
second_hash = hashlib.sha256(first_hash).digest()

calculated_hash = second_hash.hex()
hash_number = int.from_bytes(second_hash, "big")
target = int(result["target"], 16)

print("INDEPENDENT BLOCK VERIFICATION")
print("-" * 45)
print("Stored hash:    ", result["hash"])
print("Calculated hash:", calculated_hash)
print("Hash matches:   ", calculated_hash == result["hash"])
print("Below target:   ", hash_number < target)
print("Nonce:          ", result["nonce"])

if calculated_hash == result["hash"] and hash_number < target:
    print("\nRESULT: PROOF-OF-WORK VERIFIED")
else:
    print("\nRESULT: VERIFICATION FAILED")
