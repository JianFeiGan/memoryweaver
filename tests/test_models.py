import pytest
from datetime import datetime
from src.models import Memory, MemoryType


def test_memory_type_enum():
    """测试记忆类型枚举"""
    assert MemoryType.USER == "user"
    assert MemoryType.PROJECT == "project"
    assert MemoryType.FEEDBACK == "feedback"
    assert MemoryType.REFERENCE == "reference"
    assert MemoryType.TEMPORARY == "temporary"


def test_memory_creation():
    """测试创建记忆对象"""
    memory = Memory(
        type=MemoryType.USER,
        content="使用 2 空格缩进",
        source="claude-code"
    )
    assert memory.type == MemoryType.USER
    assert memory.content == "使用 2 空格缩进"
    assert memory.source == "claude-code"
    assert memory.id is not None
    assert memory.created_at is not None


def test_memory_to_dict():
    """测试记忆转字典"""
    memory = Memory(
        type=MemoryType.PROJECT,
        content="本项目使用 Next.js 14",
        metadata={"project": "my-app"}
    )
    d = memory.to_dict()
    assert d["type"] == "project"
    assert d["content"] == "本项目使用 Next.js 14"
    assert d["metadata"] == {"project": "my-app"}


def test_memory_from_dict():
    """测试从字典创建记忆"""
    d = {
        "id": "test-id",
        "type": "user",
        "content": "偏好函数式编程",
        "metadata": None,
        "source": "cursor",
        "ttl": None,
        "created_at": "2026-05-09T00:00:00",
        "updated_at": "2026-05-09T00:00:00",
        "accessed_at": "2026-05-09T00:00:00",
        "access_count": 0
    }
    memory = Memory.from_dict(d)
    assert memory.id == "test-id"
    assert memory.type == MemoryType.USER
