import pytest
from unittest.mock import MagicMock, patch
from src.memory_engine import MemoryEngine
from src.models import Memory, MemoryType


@pytest.fixture
def engine(tmp_path):
    """创建测试引擎"""
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


def test_save_memory(engine):
    """测试保存记忆"""
    memory = engine.save(
        type=MemoryType.USER,
        content="使用 2 空格缩进",
        source="claude-code"
    )
    assert memory.type == MemoryType.USER
    assert memory.content == "使用 2 空格缩进"
    assert memory.id is not None


def test_search_memory(engine):
    """测试搜索记忆"""
    engine.save(type=MemoryType.PROJECT, content="本项目使用 Next.js 14")
    engine.search_engine.search.return_value = [
        {"id": "test-id", "content": "本项目使用 Next.js 14", "metadata": {}, "distance": 0.1}
    ]
    results = engine.search("Next.js")
    assert len(results) > 0


def test_get_project_context(engine):
    """测试获取项目上下文"""
    engine.save(type=MemoryType.PROJECT, content="框架: Next.js 14", metadata={"project": "my-app"})
    engine.save(type=MemoryType.USER, content="使用 TypeScript")
    engine.save(type=MemoryType.FEEDBACK, content="回答要简洁")
    context = engine.get_project_context("my-app")
    assert "Next.js" in context
    assert "TypeScript" in context


def test_memory_priority(engine):
    """测试记忆优先级"""
    engine.save(type=MemoryType.USER, content="使用 Python 3.11")
    engine.save(type=MemoryType.PROJECT, content="本项目使用 Python 3.8", metadata={"project": "test"})
    context = engine.get_project_context("test")
    # 项目记忆应该优先
    assert "Python 3.8" in context
