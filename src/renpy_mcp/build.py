"""Build tools: compile_project, lint_project.

Wraps Ren'Py CLI commands via subprocess.
"""

import subprocess
import re
import os
import glob as glob_mod
from .config import get_python_exe, get_renpy_script


def _clear_cache(project_path: str):
    """Remove all .rpyc cache files in the game directory."""
    game_dir = os.path.join(project_path, "game")
    if not os.path.isdir(game_dir):
        return
    for rpyc in glob_mod.glob(os.path.join(game_dir, "**", "*.rpyc"), recursive=True):
        try:
            os.remove(rpyc)
        except OSError:
            pass


def compile_project(project_path: str, force: bool = False) -> dict:
    """Compile a Ren'Py project (.rpy -> .rpyc).

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        force: If True, clear .rpyc cache before compiling.

    Returns {ok: bool, errors: list[dict], raw_output: str}
    """
    if force:
        _clear_cache(project_path)
    return _run_renpy_command(project_path, "compile")


def lint_project(project_path: str) -> dict:
    """Run Ren'Py lint on a project.

    Returns {ok: bool, warnings: list[dict], raw_output: str}
    """
    return _run_renpy_command(project_path, "lint")


def _run_renpy_command(project_path: str, command: str) -> dict:
    """Execute a Ren'Py CLI command and parse output."""
    try:
        python_exe = get_python_exe()
        renpy_script = get_renpy_script()
    except FileNotFoundError as e:
        return {"ok": False, "errors": [{"message": str(e)}], "raw_output": str(e)}

    cmd = [python_exe, renpy_script, project_path, command]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=False,
            timeout=120,
            cwd=os.path.dirname(renpy_script),
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "errors": [{"message": "Command timed out (120s)"}], "raw_output": ""}
    except FileNotFoundError:
        return {"ok": False, "errors": [{"message": f"Python executable not found: {python_exe}"}], "raw_output": ""}

    try:
        out = result.stdout.decode("utf-8", errors="replace")
        err = result.stderr.decode("utf-8", errors="replace")
    except Exception:
        out = result.stdout.decode("gbk", errors="replace")
        err = result.stderr.decode("gbk", errors="replace")
    output = out + "\n" + err

    if command == "compile":
        errors = _parse_compile_errors(output)
        return {"ok": result.returncode == 0, "errors": errors, "raw_output": output}
    elif command == "lint":
        warnings = _parse_lint_output(output)
        return {"ok": result.returncode == 0, "warnings": warnings, "raw_output": output}

    return {"ok": result.returncode == 0, "raw_output": output}


def _parse_compile_errors(output: str) -> list[dict]:
    """Parse Ren'Py compile errors from CLI output."""
    errors = []
    # Ren'Py error format: File "game/script.rpy", line 42: expected ':' ...
    pattern = re.compile(
        r'File\s+"([^"]+)",\s*line\s+(\d+):\s*(.+)'
    )
    for match in pattern.finditer(output):
        errors.append({
            "file": match.group(1),
            "line": int(match.group(2)),
            "message": match.group(3).strip(),
        })

    # Also catch lines like: game/script.rpy:42: error message
    alt_pattern = re.compile(
        r'(game/[^\s:]+):(\d+):\s*(.+)'
    )
    for match in alt_pattern.finditer(output):
        errors.append({
            "file": match.group(1),
            "line": int(match.group(2)),
            "message": match.group(3).strip(),
        })

    return errors


def _parse_lint_output(output: str) -> list[dict]:
    """Parse Ren'Py lint warnings from CLI output."""
    warnings = []
    # Similar pattern to compile errors
    pattern = re.compile(
        r'(game/[^\s:]+):(\d+):\s*(.+)'
    )
    for match in pattern.finditer(output):
        warnings.append({
            "file": match.group(1),
            "line": int(match.group(2)),
            "message": match.group(3).strip(),
        })

    # Check for summary line: "Ren'Py lint found N errors"
    summary = re.search(r"found (\d+) (?:error|warning|issue)", output, re.IGNORECASE)
    if summary:
        count = int(summary.group(1))
        if count == 0 and not warnings:
            warnings.append({"message": "Lint passed with no issues."})

    return warnings
