"""BAGUET SDK v1.0.0 — Quickstart Guide.

Lossless bit-exact compression and cryptographic receipt verification.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Support running directly from repo checkout
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

try:
    import baguet
except (ImportError, FileNotFoundError):
    try:
        import baguet_sdk as baguet
    except (ImportError, FileNotFoundError):
        sys.stderr.write(
            "BAGUET SDK runtime required. Please install via: pip install baguet\n"
        )
        raise SystemExit(1)


def main() -> int:
    engine = baguet.BaguetEngine()
    data = b"Hello BAGUET v1.0.0 Enterprise Zero-Decompression Ecosystem!"
    compressed, bit_len = engine.compress_bytes(data)
    restored = engine.decompress_bytes(compressed)
    assert restored == data, "Lossless compression failed roundtrip verification"
    receipt = engine.generate_audit_receipt(data, compressed_packet=compressed)
    assert receipt["roundtrip_verified"] is True
    print(f"BAGUET Quickstart Success: {len(data)}B -> {len(compressed)}B (Reduction: {receipt['reduction_pct']:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
