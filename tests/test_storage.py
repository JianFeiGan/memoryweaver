import pytest
from src.storage import SQLiteStorage
from src.models import Memory, MemoryType


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def storage(db_path):
    return SQLiteStorage(db_path)


def test_create_and_get_memory(storage):
    """测试创建和获取记忆"""
    memory = Memory(
        type=MemoryType.USER,
        content="使用 2 空格缩进",
        source="claude-code"
    )
    storage.save(memory)
    retrieved = storage.get(memory.id)
    assert retrieved is not None
    assert retrieved.content == "使用 2 空格缩进"
    assert retrieved.type == MemoryType.USER


def test_list_memories(storage):
    """测试列出记忆"""
    for i in range(5):
        storage.save(Memory(
            type=MemoryType.USER if i % 2 == 0 else MemoryType.PROJECT,
            content=f"记忆 {i}"
        ))
    all_memories = storage.list()
    assert len(all_memories) == 5
    user_memories = storage.list(type_filter=MemoryType.USER)
    assert len(user_memories) == 3


def test_update_memory(storage):
    """测试更新记忆"""
    memory = Memory(type=MemoryType.USER, content="原始内容")
    storage.save(memory)
    memory.content = "更新后的内容"
    storage.save(memory)
    retrieved = storage.get(memory.id)
    assert retrieved.content == "更新后的内容"


def test_delete_memory(storage):
    """测试删除记忆"""
    memory = Memory(type=MemoryType.USER, content="要删除的记忆")
    storage.save(memory)
    assert storage.get(memory.id) is not None
    storage.delete(memory.id)
    assert storage.get(memory.id) is None


def test_fulltext_search(storage):
    """测试全文搜索"""
    storage.save(Memory(type=MemoryType.PROJECT, content="本项目使用 Next.js 14"))
    storage.save(Memory(type=MemoryType.PROJECT, content="数据库使用 PostgreSQL"))
    storage.save(Memory(type=MemoryType.USER, content="偏好 TypeScript"))
    results = storage.search_text("Next.js")
    assert len(results) == 1
    assert "Next.js" in results[0].content
