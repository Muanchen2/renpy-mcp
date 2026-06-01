# Changelog

## [0.2.0] — 2026-06-01

### Added
- `copy_asset` tool — copy images, fonts, audio into Ren'Py projects
- `get_image_size` tool — get image dimensions for sprite positioning
- CJK font auto-detection and configuration in `exec_rpy`
- `replace` mode in `exec_rpy` — search-and-replace text in .rpy files
- Auto-create target file in `exec_rpy` when it doesn't exist
- `force` parameter in `compile_project` — clear .rpyc cache before compile
- `AI_GUIDE.md` — operational guide for AI agents using this MCP

### Fixed
- `copy_asset` auto-prefixes `game/` to destination paths
- CJK text no longer requires manual font setup

## [0.1.0] — 2026-05-31

### Added
- Initial release with 5 core tools:
  - `list_labels` — scan project labels
  - `read_script` — read label content line-by-line
  - `exec_rpy` — universal code injection (end/top/inside/after/before)
  - `compile_project` — validate .rpy syntax
  - `lint_project` — static analysis
- Built with FastMCP
