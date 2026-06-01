"""Ren'Py SDK path configuration."""

import os

# Default Ren'Py SDK paths to try
_DEFAULT_SDK_PATHS = [
    r"D:\Software\Work-software\RenPy\renpy-8.5.3-sdk",
    r"C:\Program Files\RenPy\renpy-8.5.3-sdk",
]

_SDK_PATH: str | None = None


def get_sdk_path() -> str:
    """Get the Ren'Py SDK path. Checks env var first, then default paths."""
    global _SDK_PATH
    if _SDK_PATH:
        return _SDK_PATH

    env_path = os.environ.get("RENPY_SDK_PATH")
    if env_path and os.path.isdir(env_path):
        _SDK_PATH = env_path
        return _SDK_PATH

    for path in _DEFAULT_SDK_PATHS:
        if os.path.isdir(path):
            _SDK_PATH = path
            return _SDK_PATH

    raise FileNotFoundError(
        "Ren'Py SDK not found. Set RENPY_SDK_PATH environment variable "
        "or install Ren'Py SDK to one of the default paths."
    )


def get_python_exe() -> str:
    """Get the path to Ren'Py's embedded Python executable."""
    sdk = get_sdk_path()
    python_path = os.path.join(sdk, "lib", "py3-windows-x86_64", "python.exe")
    if os.path.isfile(python_path):
        return python_path
    raise FileNotFoundError(f"Ren'Py Python not found at: {python_path}")


def get_renpy_script() -> str:
    """Get the path to renpy.py entry script."""
    sdk = get_sdk_path()
    script_path = os.path.join(sdk, "renpy.py")
    if os.path.isfile(script_path):
        return script_path
    raise FileNotFoundError(f"renpy.py not found at: {script_path}")
