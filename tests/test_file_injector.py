import pytest
import os
from src.file_injector import FileInjector


@pytest.fixture
def injector(tmp_path):
    return FileInjector(str(tmp_path))


def test_generate_cursor_rules(injector):
    """测试生成 .cursorrules 文件"""
    context = "## 项目信息\n- 框架: Next.js 14\n\n## 开发者偏好\n- 使用 TypeScript"
    result = injector.generate("cursor", context)
    assert result["path"] == ".cursorrules"
    assert "Next.js" in result["content"]


def test_generate_claude_md(injector):
    """测试生成 CLAUDE.md 文件"""
    context = "## 项目信息\n- 数据库: PostgreSQL"
    result = injector.generate("claude", context)
    assert result["path"] == ".claude/CLAUDE.md"
    assert "PostgreSQL" in result["content"]


def test_generate_agents_md(injector):
    """测试生成 AGENTS.md 文件"""
    context = "## 行为指导\n- 回答要简洁"
    result = injector.generate("generic", context)
    assert result["path"] == "AGENTS.md"
    assert "简洁" in result["content"]


def test_write_file(injector, tmp_path):
    """测试写入文件"""
    context = "测试内容"
    result = injector.generate("generic", context)
    injector.write(result)
    file_path = tmp_path / "AGENTS.md"
    assert file_path.exists()
    assert "测试内容" in file_path.read_text()
