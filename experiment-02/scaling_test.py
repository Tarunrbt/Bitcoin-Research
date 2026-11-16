import csv
import hashlib
import os
import statistics
import struct
import time

RUNS = 30
BITS = [12, 14, 16, 18, 20]


def dsha(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def mine(bits):
    prev = bytes(32)
    merkle = os.urandom(32)  # har run alag header
    ts = int(time.time())
    target = 1 << (256 - bits)
    prefix = (struct.pack("<L", 1) + prev + merkle
              + struct.pack("<L", ts) + struct.pack("<L", bits))
    t0 = time.time()
    for nonce in range(2**32):
        if int.from_bytes(dsha(prefix + struct.pack("<L", nonce)), "big") < target:
            return nonce + 1, time.time() - t0
    return None, None


rows = []
print(f"{'bits':>4} {'expected':>10} {'mean':>10} {'median':>10} {'stdev':>10} {'mean/exp':>9}")
for bits in BITS:
    attempts = []
    for run in range(RUNS):
        n, el = mine(bits)
        attempts.append(n)
        rows.append([bits, run + 1, n, round(el, 4)])
    exp = 2 ** bits
    m = statistics.mean(attempts)
    print(f"{bits:>4} {exp:>10} {m:>10.0f} {statistics.median(attempts):>10.0f} "
          f"{statistics.stdev(attempts):>10.0f} {m/exp:>9.2f}")

with open("scaling_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bits", "run", "attempts", "seconds"])
    w.writerows(rows)

print("Saved: scaling_results.csv")
