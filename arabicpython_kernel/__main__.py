"""arabicpython_kernel/__main__.py
B-054: Install the apython Jupyter kernel spec.

Usage::

    python -m arabicpython_kernel install           # user install
    python -m arabicpython_kernel install --sys-prefix
    python -m arabicpython_kernel install --prefix /some/prefix

This writes a ``kernel.json`` and optional logo into the Jupyter kernel
data directory so the kernel appears in the JupyterLab / Notebook picker.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

KERNEL_JSON = {
    "argv": [sys.executable, "-m", "arabicpython_kernel", "-f", "{connection_file}"],
    "display_name": "لغة الثعبان (apython)",
    "language": "apy",
    "interrupt_mode": "signal",
    "metadata": {
        "debugger": False,
    },
}


def _install(prefix: str | None, sys_prefix: bool, user: bool) -> None:
    try:
        import jupyter_client  # type: ignore  # noqa: F401
    except ImportError:
        print(
            "jupyter_client is not installed. "
            "Install it with: pip install jupyter_client",
            file=sys.stderr,
        )
        sys.exit(1)

    with tempfile.TemporaryDirectory() as td:
        kernel_dir = Path(td) / "apy"
        kernel_dir.mkdir()
        (kernel_dir / "kernel.json").write_text(
            json.dumps(KERNEL_JSON, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        from jupyter_client.kernelspec import KernelSpecManager  # type: ignore

        ksm = KernelSpecManager()
        install_kwargs: dict = {"kernel_name": "apy", "user": user, "replace": True}
        if sys_prefix:
            install_kwargs["prefix"] = sys.prefix
        elif prefix:
            install_kwargs["prefix"] = prefix

        dest = ksm.install_kernel_spec(str(kernel_dir), **install_kwargs)
        print(f"Installed kernel spec: {dest}")


def _run_kernel(connection_file: str) -> None:
    """Launch the kernel (called by Jupyter when it starts a kernel process)."""
    from ipykernel.kernelapp import IPKernelApp  # type: ignore
    from arabicpython_kernel.kernel import ArabicPythonKernel

    IPKernelApp.launch_instance(
        kernel_class=ArabicPythonKernel,
        argv=["kernel", "-f", connection_file],
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m arabicpython_kernel")
    sub = parser.add_subparsers(dest="cmd")

    inst = sub.add_parser("install", help="Install the kernel spec into Jupyter.")
    inst.add_argument("--sys-prefix", action="store_true", dest="sys_prefix")
    inst.add_argument("--prefix", default=None)
    inst.add_argument("--user", action="store_true", default=True)

    # When Jupyter spawns the kernel it passes '-f <connection_file>'
    parser.add_argument("-f", dest="connection_file", default=None)

    args = parser.parse_args()

    if args.cmd == "install":
        _install(args.prefix, args.sys_prefix, args.user)
    elif args.connection_file:
        _run_kernel(args.connection_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
