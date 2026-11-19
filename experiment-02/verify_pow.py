import hashlib
import json
import struct


def double_sha256(data):
    return hashlib.sha256(
        hashlib.sha256(data).digest()
    ).digest()


with open("mining_result.json") as f:
    result = json.load(f)

header = (
    struct.pack("<L", result["version"])
    + bytes.fromhex(result["previous_hash"])
    + bytes.fromhex(result["merkle_root"])
    + struct.pack("<L", result["timestamp"])
    + struct.pack("<L", result["difficulty_bits"])
    + struct.pack("<L", result["nonce"])
)

calculated_hash = double_sha256(header).hex()
target = int(result["target"], 16)

hash_matches = calculated_hash == result["hash"]
below_target = int(calculated_hash, 16) < target

print("INDEPENDENT BLOCK VERIFICATION")
print("-" * 45)
print("Stored hash:     ", result["hash"])
print("Calculated hash: ", calculated_hash)
print("Hash matches:    ", hash_matches)
print("Below target:    ", below_target)
print("Nonce:           ", result["nonce"])

if hash_matches and below_target:
    print("\nRESULT: PROOF-OF-WORK VERIFIED")
else:
    print("\nRESULT: VERIFICATION FAILED")
