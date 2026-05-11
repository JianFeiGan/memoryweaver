# tests/test_integration.py
import pytest
from unittest.mock import MagicMock, patch
from src.memory_engine import MemoryEngine
from src.file_injector import FileInjector
from src.models import MemoryType


@pytest.fixture
def engine(tmp_path):
    """创建集成测试引擎"""
    db_path = str(tmp_path / "test.db")
    with patch("src.memory_engine.SearchEngine") as MockSearch:
        mock_search = MagicMock()
        MockSearch.return_value = mock_search
        mock_search.search.return_value = []
        eng = MemoryEngine(
            db_path=db_path,
            chroma_path=str(tmp_path / "chroma"),
            embedding_api_key="test-key"
        )
        eng.search_engine = mock_search
        yield eng


def test_save_search_context_flow(engine):
    """测试保存-搜索-上下文完整流程"""
    # 保存记忆
    engine.save(type=MemoryType.PROJECT, content="框架: Next.js 14", metadata={"project": "my-app"})
    engine.save(type=MemoryType.PROJECT, content="数据库: PostgreSQL", metadata={"project": "my-app"})
    engine.save(type=MemoryType.USER, content="使用 TypeScript")
    engine.save(type=MemoryType.FEEDBACK, content="回答要简洁")
    # 获取项目上下文
    context = engine.get_project_context("my-app")
    assert "Next.js" in context
    assert "PostgreSQL" in context
    assert "TypeScript" in context
    assert "简洁" in context


def test_file_injection_flow(engine, tmp_path):
    """测试文件注入流程"""
    engine.save(type=MemoryType.PROJECT, content="认证: NextAuth.js", metadata={"project": "my-app"})
    injector = FileInjector(str(tmp_path))
    context = engine.get_project_context("my-app")
    # 生成并写入 Claude 文件
    result = injector.generate("claude", context)
    injector.write(result)
    # 验证文件
    claude_file = tmp_path / ".claude" / "CLAUDE.md"
    assert claude_file.exists()
    content = claude_file.read_text()
    assert "NextAuth" in content


def test_memory_update_flow(engine):
    """测试记忆更新流程"""
    memory = engine.save(type=MemoryType.USER, content="原始偏好")
    engine.update(memory.id, content="更新后的偏好")
    updated = engine.get(memory.id)
    assert updated.content == "更新后的偏好"


def test_memory_delete_flow(engine):
    """测试记忆删除流程"""
    memory = engine.save(type=MemoryType.TEMPORARY, content="临时记忆")
    assert engine.get(memory.id) is not None
    engine.delete(memory.id)
    assert engine.get(memory.id) is None
