"""Public Python namespace for the BAGUET v1.0.0 SDK (core, ai, media, license, studio)."""

from __future__ import annotations

import importlib.util as _importlib_util
import sys as _sys
from pathlib import Path as _Path

_engine_path = _Path(__file__).with_name("engine-baguet.py")
_spec = _importlib_util.spec_from_file_location("_baguet_sdk_engine", _engine_path)
if _spec is None or _spec.loader is None:
    raise ImportError("BAGUET engine loader is unavailable")
_engine = _importlib_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _engine
_spec.loader.exec_module(_engine)

for _name in dir(_engine):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_engine, _name)

__version__ = "1.0.0"


def main(argv: list[str] | None = None) -> int:
    """Run the BAGUET CLI entry point."""
    arguments = list(_sys.argv[1:] if argv is None else argv)
    if arguments:
        cmd = arguments[0]
        if cmd in {"--version", "-V"}:
            print(__version__)
            return 0
        if cmd == "audit":
            arguments = ["roi-audit", *arguments[1:]]
        elif cmd in {"activate", "Activate-Baguet"}:
            return activate_main(arguments[1:])
        elif cmd in {"verify-readiness", "readiness"}:
            return int(_engine.run_cli(["release", "verify-readiness", *arguments[1:]]))
    return int(_engine.run_cli(arguments))


def activate_main(argv: list[str] | None = None) -> int:
    """Run the Activate-Baguet CLI entry point to activate a license token."""
    arguments = _sys.argv[1:] if argv is None else argv
    if not arguments or arguments[0] in {"-h", "--help"}:
        print("Usage: Activate-Baguet TOKEN [--no-persist] [--kid KID]", file=_sys.stderr)
        return 0 if arguments and arguments[0] in {"-h", "--help"} else 2
    token = arguments[0]
    extra = arguments[1:]
    if token in {"--token", "-t"} and len(arguments) > 1:
        token = arguments[1]
        extra = arguments[2:]
    return int(_engine.run_cli(["license", "activate", token, *extra]))


def studio_main() -> int:
    """Launch the local BAGUET Studio dashboard."""
    return int(_engine.run_cli(["studio"]))


def landing_main() -> int:
    """Launch the local BAGUET Landing page."""
    return int(_engine.run_cli(["landing"]))


def desktop_compress_main() -> int:
    """Compress one selected file to a sibling .bgt without overwriting output."""
    arguments = _sys.argv[1:]
    if len(arguments) != 1:
        print("Usage: baguet-desktop-compress INPUT_FILE", file=_sys.stderr)
        return 2
    source = _Path(arguments[0]).expanduser()
    if source.is_symlink() or not source.is_file():
        print("BAGUET: input must be a regular, non-symlink file.", file=_sys.stderr)
        return 2
    output = source.with_name(source.name + ".bgt")
    if output.exists() or output.is_symlink():
        print(f"BAGUET: refusing to overwrite existing output: {output}", file=_sys.stderr)
        return 2
    return int(_engine.run_cli(["compress", str(source), str(output)]))


_engine.activate_main = activate_main

if __name__ == "__main__":
    raise SystemExit(main())
