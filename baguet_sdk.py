"""Public Python namespace for the BAGUET SDK.

The frozen engine remains the implementation source. This module loads it from
the adjacent file so source checkouts and clean-room distributions expose the
same import name without duplicating engine state.
"""

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


def main() -> int:
    """Run the BAGUET CLI entry point."""
    return int(_engine.run_cli())


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


if __name__ == "__main__":
    raise SystemExit(main())
