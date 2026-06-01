"""Project structure tools: list_labels, read_script."""

import os
import re
import glob as glob_mod
from dataclasses import dataclass, asdict


@dataclass
class LabelInfo:
    name: str
    file: str
    line: int


def list_labels(project_path: str) -> list[dict]:
    """Scan all .rpy files in a Ren'Py project and list all labels.

    Returns a list of {name, file, line} dicts.
    """
    labels: list[dict] = []
    rpy_dir = os.path.join(project_path, "game")

    if not os.path.isdir(rpy_dir):
        return labels

    pattern = re.compile(r"^\s*label\s+(\w+)\s*(?:\(.*?\))?\s*:")

    for filepath in glob_mod.glob(os.path.join(rpy_dir, "**", "*.rpy"), recursive=True):
        rel_path = os.path.relpath(filepath, project_path)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    m = pattern.match(line)
                    if m:
                        labels.append(asdict(LabelInfo(
                            name=m.group(1),
                            file=rel_path,
                            line=line_no,
                        )))
        except (IOError, UnicodeDecodeError):
            continue

    return labels


def read_script(project_path: str, label_name: str) -> str:
    """Read the content of a specific label from a Ren'Py project.

    Returns the complete script block under the label, or empty string if not found.
    """
    rpy_dir = os.path.join(project_path, "game")
    label_pattern = re.compile(rf"^\s*label\s+{re.escape(label_name)}\s*(?:\(.*?\))?\s*:")
    dedent_pattern = re.compile(r"^(\s*)(\S)")

    for filepath in glob_mod.glob(os.path.join(rpy_dir, "**", "*.rpy"), recursive=True):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except (IOError, UnicodeDecodeError):
            continue

        for i, line in enumerate(lines):
            if label_pattern.match(line):
                return _extract_label_block(lines, i)

    return ""


def _extract_label_block(lines: list[str], start_idx: int) -> str:
    """Extract all lines belonging to a label block (same or deeper indentation)."""
    result = [lines[start_idx]]

    # Determine the base indentation for content inside the label
    # Label line itself is at 0 indentation (or some base)
    # Content lines must be indented deeper than the label line
    label_line = lines[start_idx]
    label_indent = len(label_line) - len(label_line.lstrip())

    for i in range(start_idx + 1, len(lines)):
        line = lines[i]
        stripped = line.strip()

        # Empty line or comment: always include
        if not stripped or stripped.startswith("#"):
            result.append(line)
            continue

        # Check indentation
        line_indent = len(line) - len(line.lstrip())

        # If this line is at or shallower than label indent, it's a new block
        if line_indent <= label_indent and stripped:
            break

        result.append(line)

    return "".join(result).rstrip() + "\n"
