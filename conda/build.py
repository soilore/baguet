"""Install the SDK from a signed clean-room distribution into Conda."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(os.environ.get("SRC_DIR", Path(__file__).resolve().parents[1])).resolve()
    prefix = Path(os.environ["PREFIX"]).resolve()
    public_value = os.environ.get("BAGUET_PUBLIC_DIST_DIR")
    trusted_key = os.environ.get("BAGUET_ROOT_PUBKEY_HEX")
    if not public_value or not trusted_key:
        raise RuntimeError(
            "BAGUET_PUBLIC_DIST_DIR and BAGUET_ROOT_PUBKEY_HEX are required; "
            "Conda packaging refuses private source or untrusted native artifacts"
        )
    public_dist = Path(public_value).expanduser().resolve(strict=True)
    if public_dist.is_relative_to(root) or not public_dist.is_dir():
        raise RuntimeError("BAGUET_PUBLIC_DIST_DIR must point outside the private source checkout")
    if not prefix.is_dir():
        raise RuntimeError("PREFIX must be an initialized Conda environment")

    environment = os.environ.copy()
    environment["BAGUET_PUBLIC_DIST_DIR"] = str(public_dist)
    environment["BAGUET_ROOT_PUBKEY_HEX"] = trusted_key
    environment.setdefault("BAGUET_ROOT_KEY_ID", "bgt-root-2026-01")
    subprocess.run(
        [
            sys.executable, "-m", "pip", "install", "--no-deps",
            "--no-build-isolation", "--no-cache-dir", str(root),
        ],
        cwd=root,
        env=environment,
        check=True,
    )


if __name__ == "__main__":
    main()
