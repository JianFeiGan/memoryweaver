import pytest
from unittest.mock import MagicMock, patch
from src.auto_extractor import AutoExtractor
from src.models import MemoryType


@pytest.fixture
def extractor():
    with patch("src.auto_extractor.openai") as mock:
        client = MagicMock()
        mock.OpenAI.return_value = client
        yield AutoExtractor(api_key="test-key", model="deepseek-chat")


def test_extract_memories(extractor):
    """测试从对话提取记忆"""
    conversation = """
    用户: 这个项目用什么框架?
    助手: 本项目使用 Next.js 14 App Router。
    用户: 我习惯用 TypeScript strict 模式。
    助手: 好的，已记住。
    """
    # 模拟 API 响应
    extractor.client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='''[
            {"type": "project", "content": "本项目使用 Next.js 14 App Router", "confidence": 0.9},
            {"type": "user", "content": "习惯用 TypeScript strict 模式", "confidence": 0.85}
        ]'''))]
    )
    memories = extractor.extract(conversation)
    assert len(memories) == 2
    assert memories[0].type == MemoryType.PROJECT
    assert memories[1].type == MemoryType.USER


def test_extract_with_project(extractor):
    """测试带项目名的提取"""
    conversation = "用户: 数据库用 PostgreSQL"
    extractor.client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='''[
            {"type": "project", "content": "数据库使用 PostgreSQL", "confidence": 0.95}
        ]'''))]
    )
    memories = extractor.extract(conversation, project="my-app")
    assert memories[0].metadata.get("project") == "my-app"
