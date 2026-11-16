import hashlib
import json
import struct
import sys
import time


def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def mine_block(difficulty_bits: int = 20):
    version = 1
    previous_hash = "00" * 32
    merkle_root = hashlib.sha256(b"Shield EPC demo transaction").hexdigest()
    timestamp = int(time.time())

    # Target: hash is valid if its integer value is below this
    target = 1 << (256 - difficulty_bits)

    header_prefix = (
        struct.pack("<L", version)
        + bytes.fromhex(previous_hash)
        + bytes.fromhex(merkle_root)
        + struct.pack("<L", timestamp)
        + struct.pack("<L", difficulty_bits)
    )

    print(f"Mining started | difficulty_bits = {difficulty_bits}")
    start = time.time()
    attempts = 0

    for nonce in range(2**32):
        attempts += 1
        digest = double_sha256(header_prefix + struct.pack("<L", nonce))

        if int.from_bytes(digest, "big") < target:
            elapsed = time.time() - start

            result = {
                "version": version,
                "previous_hash": previous_hash,
                "merkle_root": merkle_root,
                "timestamp": timestamp,
                "difficulty_bits": difficulty_bits,
                "nonce": nonce,
                "hash": digest.hex(),
                "target": hex(target),
                "attempts": attempts,
                "elapsed_seconds": elapsed,
                "hashes_per_second": attempts / elapsed if elapsed > 0 else None
            }

            with open("mining_result.json", "w") as f:
                json.dump(result, f, indent=4)

            print(json.dumps(result, indent=4))
            return result

    print("Nonce space exhausted.")
    return None


if __name__ == "__main__":

    difficulty = (
        int(sys.argv[1]) if len(sys.argv) > 1 else 20
    )

    mine_block(difficulty)
