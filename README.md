# Bitcoin Research

Hands-on experiments to understand Bitcoin's core mechanics from first principles, in Python.

## Experiments

| # | Topic | Status |
|---|-------|--------|
| 01 | SHA-256 behaviour | Done |
| 02 | Proof-of-Work mining simulation | Done |
| 03 | Blockchain construction & tamper detection | Planned |

## Experiment 02: Proof-of-Work

- SHA-256d hashing with nonce-based mining
- Difficulty-target verification and independent PoW verifier
- Binary header hash recomputation

**Statistical test:** 30 independent runs per difficulty (150 trials total).

| Difficulty (bits) | Expected 2^d | Observed mean |
|---|---|---|
| 12 | 4,096 | 3,931 |
| 14 | 16,384 | 12,290 |
| 16 | 65,536 | 71,438 |
| 18 | 262,144 | 248,331 |
| 20 | 1,048,576 | 991,179 |

Observed means match E[N] = 2^d within expected sampling variance
(SE ≈ mean/√30). Each +2 bits of difficulty means ~4x more work.

## Run

    cd experiment-02
    python3 -m venv .venv && source .venv/bin/activate
    python pow_mining.py
    python verify_pow.py mining_result.json
    python scaling_test.py

## Limitations

Educational simulation, not a full Bitcoin consensus implementation
(no networking, mempool, difficulty retargeting or Merkle trees).
