"""Ren'Py MCP Server - registers all tools with FastMCP."""

import sys
import os

# Ensure src is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from renpy_mcp.project import list_labels, read_script
from renpy_mcp.executor import exec_rpy
from renpy_mcp.build import compile_project, lint_project
from renpy_mcp.assets import copy_asset, get_image_size

mcp = FastMCP("Ren'Py MCP")


@mcp.tool()
def tool_list_labels(project_path: str) -> list[dict]:
    """List all labels in a Ren'Py project.

    Scans all .rpy files under project_path/game/ and returns label names,
    their source files, and line numbers.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
    """
    return list_labels(project_path)


@mcp.tool()
def tool_read_script(project_path: str, label_name: str) -> str:
    """Read the script content of a specific label.

    Returns the complete Ren'Py script block under the given label,
    including all dialogue, menus, and nested logic.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        label_name: The label name to read (e.g. "start", "chapter_01").
    """
    return read_script(project_path, label_name)


@mcp.tool()
def tool_exec_rpy(
    project_path: str,
    file: str,
    code: str,
    position: str = "end",
    auto_compile: bool = True,
) -> dict:
    """Inject arbitrary Ren'Py code into a project file.

    This is the universal "escape hatch" tool. Use it to write any Ren'Py
    script code: define characters, declare images, create screens, add
    dialogue to labels, write init python blocks, etc.

    Automatically detects CJK text and configures a compatible font if needed.
    If the target file doesn't exist, it will be auto-created.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        file: Target .rpy file, relative to project_path (e.g. "game/script.rpy").
        code: Raw Ren'Py script code to inject.
        position: Where to place the code:
            - "end": Append at end of file (default)
            - "top": Prepend at start of file
            - "inside:<label>": Insert at end of a label block
            - "after:<label>": Insert right after a label block ends
            - "before:<label>": Insert right before a label definition
            - "replace:<old_text>": Replace first occurrence of old_text with code
        auto_compile: Whether to run compile_project after writing (default True).

    Returns:
        dict with {ok, message, compile_result}.
    """
    return exec_rpy(project_path, file, code, position, auto_compile)


@mcp.tool()
def tool_compile_project(project_path: str, force: bool = False) -> dict:
    """Compile a Ren'Py project (validate syntax).

    Runs Ren'Py's compiler on all .rpy files. Returns structured errors
    with file paths and line numbers if compilation fails.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        force: If True, clear .rpyc cache before compiling (to pick up file changes).

    Returns:
        dict with {ok: bool, errors: [{file, line, message}], raw_output: str}.
    """
    return compile_project(project_path, force)


@mcp.tool()
def tool_lint_project(project_path: str) -> dict:
    """Run Ren'Py lint on a project (static analysis).

    Checks for undefined variables, unreachable code, missing labels, etc.
    More thorough than compile but may produce false positives.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.

    Returns:
        dict with {ok: bool, warnings: [{file, line, message}], raw_output: str}.
    """
    return lint_project(project_path)


@mcp.tool()
def tool_copy_asset(project_path: str, source: str, dest: str) -> dict:
    """Copy an asset file (image, font, audio) into a Ren'Py project.

    Copies a file from anywhere on the system into the project's game directory.
    Automatically creates subdirectories as needed.
    Auto-prefixes 'game/' to dest if not already present.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        source: Absolute path to the source file on disk.
        dest: Relative path within project (e.g. "images/char_happy.png").

    Returns:
        dict with {ok, message, dest_path}.
    """
    return copy_asset(project_path, source, dest)


@mcp.tool()
def tool_get_image_size(project_path: str, image_path: str) -> dict:
    """Get dimensions and format of an image file.

    Useful for calculating correct sprite positioning transforms.
    Supports absolute paths or paths relative to project_path.

    Args:
        project_path: Absolute path to the Ren'Py project root directory.
        image_path: Path to image file (absolute, or relative to project_path).

    Returns:
        dict with {ok, width, height, format, file_size}.
    """
    return get_image_size(project_path, image_path)


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
