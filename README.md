# MemoryWeaver

> **统一 Agent 记忆中枢 / Universal Agent Memory Hub**

[English](#english) | [中文](#中文)

---

## English

### Overview

MemoryWeaver is a unified memory management MCP Server for AI coding agents. It solves the "memory island" problem where switching between tools (Claude Code, Cursor, Trae, Hermes, etc.) loses context and requires re-configuring your preferences.

### Features

- **Multiple Memory Types**: user / project / feedback / reference / temporary
- **Semantic Search**: Vector search powered by ChromaDB
- **Full-text Search**: SQLite FTS5 for exact matching
- **Auto-extraction**: Extract memories from conversations using DeepSeek API
- **File Injection**: Generate context files for Cursor / Claude Code / generic agents

### Installation

```bash
# Clone the repository
git clone https://github.com/JianFeiGan/memoryweaver.git
cd memoryweaver

# Install dependencies
uv sync
```

### Configuration

Copy `config.example.yaml` to `config.yaml` and fill in your API keys:

```bash
cp config.example.yaml config.yaml
```

Environment variable substitution is supported using `${ENV_VAR}` syntax:

```yaml
api:
  embedding:
    api_key: "${OPENAI_API_KEY}"
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
```

### Usage

#### Start the MCP Server

```bash
uv run python -m src.server
```

#### Configure in Claude Code

Add to your MCP settings:

```json
{
  "mcpServers": {
    "memoryweaver": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/MemoryWeaver"
    }
  }
}
```

#### Configure in Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "memoryweaver": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/MemoryWeaver"
    }
  }
}
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `save_memory` | Save a memory with type, content, and metadata |
| `search_memory` | Search memories (semantic + full-text) |
| `list_memories` | List memories with optional filters |
| `get_project_context` | Get formatted project context for injection |
| `extract_from_conversation` | Auto-extract memories from conversation |

### Testing

```bash
uv run pytest tests/ -v
```

### Architecture

```
MemoryWeaver/
├── src/
│   ├── server.py              # MCP Server entry point
│   ├── memory_engine.py       # Core memory engine
│   ├── auto_extractor.py      # Auto-extraction module
│   ├── search_engine.py       # Search engine (semantic + full-text)
│   ├── file_injector.py       # File injection module
│   ├── models.py              # Data models
│   └── config.py              # Configuration
├── tests/                     # Test suite
├── pyproject.toml             # Project config
└── config.yaml                # Runtime config
```

### Tech Stack

- **Python 3.11+**
- **MCP SDK** - Model Context Protocol
- **SQLite** - Metadata storage
- **ChromaDB** - Vector storage
- **OpenAI API** - Embeddings
- **DeepSeek API** - Auto-extraction

### License

MIT

---

## 中文

### 概述

MemoryWeaver 是一个统一的 AI 编码 Agent 记忆管理 MCP Server。它解决了"记忆孤岛"问题——在 Claude Code、Cursor、Trae、Hermes 等工具之间切换时丢失上下文，需要重新配置偏好设置。

### 功能特性

- **多种记忆类型**: 个人记忆 / 项目记忆 / 反馈记忆 / 引用记忆 / 临时记忆
- **语义搜索**: 基于 ChromaDB 的向量搜索，理解查询意图
- **全文搜索**: 基于 SQLite FTS5 的精确匹配
- **自动提炼**: 使用 DeepSeek API 从对话中自动提取记忆
- **文件注入**: 为 Cursor / Claude Code / 通用 Agent 生成上下文文件

### 安装

```bash
# 克隆仓库
git clone https://github.com/JianFeiGan/memoryweaver.git
cd memoryweaver

# 安装依赖
uv sync
```

### 配置

复制 `config.example.yaml` 为 `config.yaml`，填入你的 API Key:

```bash
cp config.example.yaml config.yaml
```

支持环境变量替换，使用 `${ENV_VAR}` 语法:

```yaml
api:
  embedding:
    api_key: "${OPENAI_API_KEY}"
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
```

### 使用方法

#### 启动 MCP Server

```bash
uv run python -m src.server
```

#### 在 Claude Code 中配置

添加到 MCP 设置:

```json
{
  "mcpServers": {
    "memoryweaver": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/MemoryWeaver"
    }
  }
}
```

#### 在 Cursor 中配置

添加到 `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "memoryweaver": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/MemoryWeaver"
    }
  }
}
```

### MCP 工具

| 工具 | 说明 |
|------|------|
| `save_memory` | 保存记忆，支持类型、内容和元数据 |
| `search_memory` | 搜索记忆 (语义搜索 + 全文搜索) |
| `list_memories` | 列出记忆，支持按类型/项目过滤 |
| `get_project_context` | 获取格式化的项目上下文，用于文件注入 |
| `extract_from_conversation` | 从对话中自动提取记忆 |

### 测试

```bash
uv run pytest tests/ -v
```

### 项目架构

```
MemoryWeaver/
├── src/
│   ├── server.py              # MCP Server 入口
│   ├── memory_engine.py       # 核心记忆引擎
│   ├── auto_extractor.py      # 自动提炼模块
│   ├── search_engine.py       # 搜索引擎 (语义 + 全文)
│   ├── file_injector.py       # 文件注入模块
│   ├── models.py              # 数据模型
│   └── config.py              # 配置管理
├── tests/                     # 测试套件
├── pyproject.toml             # 项目配置
└── config.yaml                # 运行时配置
```

### 技术栈

- **Python 3.11+**
- **MCP SDK** - Model Context Protocol
- **SQLite** - 元数据存储
- **ChromaDB** - 向量存储
- **OpenAI API** - 文本嵌入
- **DeepSeek API** - 自动提炼

### 许可证

MIT
