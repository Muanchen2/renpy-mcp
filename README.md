# Ren'Py MCP Server

[English](#english) | [中文](#chinese)

联络网址、communicate website：https://space.bilibili.com/341162425?spm_id_from=333.788.0.0
email：1409634020@qq.com

---

## English

An MCP (Model Context Protocol) server that lets AI agents interact with Ren'Py visual novel projects — read scripts, inject code, and validate everything automatically.

Built with [FastMCP](https://github.com/jlowin/fastmcp).

### Why?

Ren'Py has no built-in editor. Developers manually write `.rpy` text files and click "Launch Project" to test. This MCP turns any AI agent (Claude, OpenCode,OpenClaw etc.) into a native Ren'Py development assistant — you describe what you want in natural language, the AI writes valid Ren'Py script, inserts it at the right location, and auto-compiles to verify.

### Tools

| Tool | Description |
|------|-------------|
| `list_labels` | Scan a project and list all labels |
| `read_script` | Read the full script content of a specific label |
| `exec_rpy` | Inject/replace Ren'Py code (7 positioning modes, auto-creates files, CJK font auto-setup) |
| `compile_project` | Compile .rpy files with optional forced cache clear |
| `lint_project` | Run static analysis on a project |
| `copy_asset` | Copy images, fonts, audio into a project (auto game/ prefix) |
| `get_image_size` | Get image dimensions for sprite positioning calculations |

### Quick Start

```bash
# Clone
git clone https://github.com/Muanchen2/renpy-mcp.git
cd renpy-mcp

# Install
python -m venv .venv
.venv\Scripts\pip install -e .

# Run
.venv\Scripts\python -m renpy_mcp.server
```

### MCP Config

Add to `~/.workbuddy/mcp.json`:

```json
{
  "mcpServers": {
    "renpy-mcp": {
      "command": "D:\\path\\to\\renpy-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "renpy_mcp.server"],
      "env": {
        "PYTHONPATH": "D:\\path\\to\\renpy-mcp\\src"
      }
    }
  }
}
```

### Requirements

- Python 3.12+
- Ren'Py SDK 8.0+ (for `compile_project` and `lint_project`)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### License

MIT — see [LICENSE](LICENSE)

---

## 中文

一个 MCP（模型上下文协议）服务器，让 AI Agent 能够操作 Ren'Py 视觉小说项目——读取脚本、注入代码、自动编译验证。

基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建。

### 为什么做这个？

Ren'Py 没有内置编辑器，开发者需要手动编写 `.rpy` 文本文件，然后点「启动项目」测试。这个 MCP 让任何 AI Agent 都可以成为 Ren'Py 的原生开发助手——你用自然语言描述需求，AI 生成正确的 Ren'Py 脚本、插入到正确位置、自动编译验证。

### 7 个工具

| 工具 | 功能 |
|------|------|
| `list_labels` | 扫描项目，列出所有 label |
| `read_script` | 读取指定 label 的完整脚本 |
| `exec_rpy` | 注入/替换 Ren'Py 代码（7种定位，自动建文件，CJK字体自动配置） |
| `compile_project` | 编译 .rpy 文件，支持强制清缓存 |
| `lint_project` | 静态分析项目代码质量 |
| `copy_asset` | 拷贝图片/字体/音频到项目（自动补 game/ 前缀） |
| `get_image_size` | 获取图片尺寸，用于立绘位置计算 |

> ⚠️ **AI Agent 使用前请先阅读 [AI_GUIDE.md](AI_GUIDE.md)** —— 包含完整工作流、常见坑和 9 大禁止事项。

### 快速开始

同上 English 部分。

### 演示流程

1. 用 `list_labels` 查看项目结构
2. 用 `read_script` 阅读现有脚本
3. 用 `exec_rpy` 注入新对话/角色/image/screen
4. 用 `compile_project` 验证语法
5. 在 Ren'Py Launcher 点「Launch Project」看效果

### 要求

- Python 3.12+
- Ren'Py SDK 8.0+
- MCP Python SDK

### 许可证

MIT
