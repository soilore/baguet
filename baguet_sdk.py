"""Public Python namespace for the BAGUET 1.0 SDK (core, ai, media, license, studio)."""

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

from baguet_sdk_layer import (  # noqa: E402
    decompress_container,
    decompress_universal_container,
    load_baguet_config,
    resolve_baguet_config_path,
    uninstall_baguet_package,
    update_baguet_config,
)

_SDK_CONFIG_EXPORTS = (
    decompress_container,
    decompress_universal_container,
    load_baguet_config,
    resolve_baguet_config_path,
    uninstall_baguet_package,
    update_baguet_config,
)

__version__ = "1.0.1"


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
        elif cmd in {"desktop-action", "one-click", "action"}:
            return desktop_action_main(arguments[1:])
        elif cmd in {"desktop-decompress", "decompress-desktop"}:
            return desktop_decompress_main()
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


def desktop_action_main(argv: list[str] | None = None) -> int:
    """Unified desktop 1-click action entry point for files and folders."""
    arguments = list(_sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in {"desktop-action", "one-click", "action"}:
        arguments = arguments[1:]
    import argparse
    from baguet_sdk_layer import desktop_one_click_action
    parser = argparse.ArgumentParser(prog="baguet desktop-action")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--mode", default="auto", choices=["auto", "compress", "decompress"])
    parser.add_argument("--lang", default=None)
    parser.add_argument("--key", default=None)
    parser.add_argument("--prior", default=None)
    parser.add_argument("--no-reveal", dest="reveal", action="store_false", default=True)
    parser.add_argument("--no-notify", dest="notify", action="store_false", default=True)
    try:
        opts = parser.parse_args(arguments)
        res = desktop_one_click_action(
            opts.paths,
            mode=opts.mode,
            lang=opts.lang,
            reveal=opts.reveal,
            notify=opts.notify,
            passphrase=opts.key,
            prior_path=opts.prior,
        )
        if res.get("action") == "open_studio_inspector":
            return 10
        return 0 if res.get("success", False) else 1
    except Exception as e:
        print(f"Baguet desktop-action error: {e}", file=_sys.stderr)
        return 1


def desktop_decompress_main() -> int:
    """1-Click decompression entry point."""
    return desktop_action_main(["--mode", "decompress", *_sys.argv[1:]])


def desktop_compress_main() -> int:
    """Compress or decompress selected files with 1-click support."""
    arguments = _sys.argv[1:]
    if any(a in {"--smart", "--mode", "--decompress", "--compress"} for a in arguments):
        return desktop_action_main(arguments)
    if len(arguments) != 1:
        print("Usage: baguet-desktop-compress INPUT_FILE", file=_sys.stderr)
        return 2
    source = _Path(arguments[0]).expanduser()
    if source.is_symlink() or not source.is_file():
        print("BAGUET: input must be a regular, non-symlink file.", file=_sys.stderr)
        return 2
    max_single_bytes = int(getattr(_engine.BaguetEngine, "MAX_DECOMPRESSED_BYTES", 67_108_864))
    ext = ".bgts" if source.stat().st_size > max_single_bytes else ".bgt"
    output = source.with_name(source.name + ext)
    if output.exists() or output.is_symlink():
        print(f"BAGUET: refusing to overwrite existing output: {output}", file=_sys.stderr)
        return 2
    return int(_engine.run_cli(["compress", str(source), str(output)]))


setattr(_engine, "activate_main", activate_main)

if __name__ == "__main__":
    raise SystemExit(main())
