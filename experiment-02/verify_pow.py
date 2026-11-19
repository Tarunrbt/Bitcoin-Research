import hashlib
import json
import struct
import sys


def double_sha256(data):
    return hashlib.sha256(
        hashlib.sha256(data).digest()
    ).digest()


def verify_block(path):
    with open(path) as f:
        result = json.load(f)

    difficulty = result["difficulty_bits"]

    if not isinstance(difficulty, int) or not 0 <= difficulty <= 256:
        raise ValueError("Invalid difficulty_bits")

    expected_target = 1 << (256 - difficulty)
    stored_target = int(result["target"], 16)

    target_matches = stored_target == expected_target

    header = (
        struct.pack("<L", result["version"])
        + bytes.fromhex(result["previous_hash"])
        + bytes.fromhex(result["merkle_root"])
        + struct.pack("<L", result["timestamp"])
        + struct.pack("<L", difficulty)
        + struct.pack("<L", result["nonce"])
    )

    calculated_hash = double_sha256(header).hex()

    hash_matches = calculated_hash == result["hash"]
    below_target = int(calculated_hash, 16) < expected_target

    print("INDEPENDENT BLOCK VERIFICATION")
    print("-" * 45)
    print("Stored hash:     ", result["hash"])
    print("Calculated hash: ", calculated_hash)
    print("Hash matches:    ", hash_matches)
    print("Target matches:  ", target_matches)
    print("Below target:    ", below_target)

    passed = hash_matches and target_matches and below_target

    print(
        "\nRESULT: PROOF-OF-WORK VERIFIED"
        if passed
        else "\nRESULT: VERIFICATION FAILED"
    )

    return passed


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "mining_result.json"

    try:
        success = verify_block(path)
        sys.exit(0 if success else 1)
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print(f"VERIFICATION ERROR: {error}")
        sys.exit(1)
