"""Build wheels only from a signed, clean-room public distribution."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


def _expected_native_name() -> str:
    if os.name == "nt":
        return "baguet_rust_core.dll"
    if sys.platform == "darwin":
        return "libbaguet_rust_core.dylib"
    if sys.platform.startswith("linux"):
        return "libbaguet_rust_core.so"
    raise RuntimeError("unsupported BAGUET wheel target")


def _validated_public_distribution() -> Path:
    configured = os.environ.get("BAGUET_PUBLIC_DIST_DIR")
    if not configured:
        raise RuntimeError(
            "BAGUET_PUBLIC_DIST_DIR is required; refusing to package private engine sources"
        )
    root = Path(configured).expanduser().resolve(strict=True)
    repository = Path(__file__).resolve().parent
    if root.is_relative_to(repository) or not root.is_dir():
        raise RuntimeError("BAGUET_PUBLIC_DIST_DIR must be an external public distribution directory")
    native_name = _expected_native_name()
    expected_files = {
        "engine-baguet.py", "engine-baguet.pyc", "baguet_sdk.py",
        "DIST-INTEGRITY.json", native_name,
    }
    if {entry.name for entry in root.iterdir()} != expected_files:
        raise RuntimeError("public distribution has an unexpected file inventory")
    for name in expected_files:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"public distribution member is not a regular file: {name}")

    trusted_hex = os.environ.get("BAGUET_ROOT_PUBKEY_HEX", "")
    expected_kid = os.environ.get("BAGUET_ROOT_KEY_ID", "bgt-root-2026-01")
    try:
        trusted_public_key = bytes.fromhex(trusted_hex)
    except ValueError as exc:
        raise RuntimeError("BAGUET_ROOT_PUBKEY_HEX must contain the trusted 32-byte public key") from exc
    if len(trusted_public_key) != 32:
        raise RuntimeError("BAGUET_ROOT_PUBKEY_HEX must contain the trusted 32-byte public key")

    manifest_path = root / "DIST-INTEGRITY.json"
    manifest_bytes = manifest_path.read_bytes()
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        canonical_manifest = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        if manifest_bytes != canonical_manifest:
            raise ValueError("non-canonical manifest")
        if not isinstance(manifest, dict) or set(manifest) != {"schema", "kid", "files", "signature"}:
            raise ValueError("manifest schema")
        if manifest["schema"] != 1 or manifest["kid"] != expected_kid:
            raise ValueError("untrusted release root")
        files = manifest["files"]
        expected_members = expected_files - {"DIST-INTEGRITY.json"}
        if not isinstance(files, dict) or set(files) != expected_members:
            raise ValueError("manifest inventory")
        unsigned = {"schema": manifest["schema"], "kid": manifest["kid"], "files": files}
        signed_bytes = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
        signature = base64.b64decode(manifest["signature"], validate=True)
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        Ed25519PublicKey.from_public_bytes(trusted_public_key).verify(signature, signed_bytes)
        if len(signature) != 64:
            raise ValueError("signature length")
        for name in sorted(expected_members):
            digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
            if not isinstance(files[name], str) or digest != files[name]:
                raise ValueError(f"member hash: {name}")
    except Exception as exc:
        raise RuntimeError("BAGUET public distribution signature or integrity verification failed") from exc
    return root


class BuildPyFromSignedDistribution(build_py):
    def run(self) -> None:
        distribution = _validated_public_distribution()
        super().run()
        destination = Path(self.build_lib)
        for name in (
            "engine-baguet.py", "engine-baguet.pyc", "baguet_sdk.py",
            _expected_native_name(), "DIST-INTEGRITY.json",
        ):
            shutil.copy2(distribution / name, destination / name)


setup(cmdclass={"build_py": BuildPyFromSignedDistribution})
