"""Asset management tool: copy_asset.

Copy images, fonts, audio, and other resource files into a Ren'Py project
game directory, with automatic directory creation.
"""

import os
import shutil


def copy_asset(project_path: str, source: str, dest: str) -> dict:
    """Copy an asset file into a Ren'Py project's game directory.

    Args:
        project_path: Root directory of the Ren'Py project.
        source: Absolute path to the source file (image, font, audio, etc.).
        dest: Relative path within project (e.g. "game/images/char_happy.png").

    Returns:
        dict with {ok, message, dest_path}
    """
    if not os.path.isfile(source):
        return {"ok": False, "message": f"Source file not found: {source}", "dest_path": None}

    # Auto-prefix game/ if not already there (Ren'Py assets live under game/)
    dest_normalized = dest.replace("\\", "/")
    if not dest_normalized.startswith("game/"):
        dest = os.path.join("game", dest)

    dest_path = os.path.join(project_path, dest)

    # Safety: only allow writing into the project directory
    real_project = os.path.realpath(project_path)
    real_dest = os.path.realpath(dest_path)
    if not real_dest.startswith(real_project + os.sep):
        return {"ok": False, "message": f"Destination outside project: {dest}", "dest_path": None}

    # Create parent directories
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    # Copy with metadata
    try:
        shutil.copy2(source, dest_path)
    except (IOError, OSError) as e:
        return {"ok": False, "message": f"Copy failed: {e}", "dest_path": None}

    file_size = os.path.getsize(dest_path)
    return {
        "ok": True,
        "message": f"Copied to {dest} ({file_size:,} bytes)",
        "dest_path": dest_path,
    }


def get_image_size(project_path: str, image_path: str) -> dict:
    """Get the dimensions and format of an image file.

    Args:
        project_path: Root directory of the Ren'Py project.
        image_path: Path to image, relative to project_path or absolute.

    Returns:
        dict with {ok, width, height, format, file_size}
    """
    if not os.path.isabs(image_path):
        image_path = os.path.join(project_path, image_path)

    if not os.path.isfile(image_path):
        return {"ok": False, "message": f"Image not found: {image_path}"}

    try:
        from PIL import Image
        with Image.open(image_path) as img:
            return {
                "ok": True,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "file_size": os.path.getsize(image_path),
            }
    except ImportError:
        # Fallback: just file info, no dimensions
        return {
            "ok": True,
            "width": None,
            "height": None,
            "format": os.path.splitext(image_path)[1].upper(),
            "file_size": os.path.getsize(image_path),
            "warning": "Pillow not installed, dimensions unavailable",
        }
    except Exception as e:
        return {"ok": False, "message": str(e)}
