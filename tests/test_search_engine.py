import pytest
from unittest.mock import MagicMock, patch
from src.search_engine import SearchEngine
from src.models import Memory, MemoryType


@pytest.fixture
def mock_chroma():
    """模拟 ChromaDB"""
    with patch("src.search_engine.chromadb") as mock:
        client = MagicMock()
        collection = MagicMock()
        mock.PersistentClient.return_value = client
        client.get_or_create_collection.return_value = collection
        # 模拟查询结果
        collection.query.return_value = {
            "ids": [["id1", "id2"]],
            "documents": [["记忆1", "记忆2"]],
            "metadatas": [[{"type": "user"}, {"type": "project"}]],
            "distances": [[0.1, 0.3]]
        }
        yield collection


@pytest.fixture
def mock_embedding():
    """模拟 Embedding API"""
    with patch("src.search_engine.openai") as mock:
        client = MagicMock()
        mock.OpenAI.return_value = client
        client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )
        yield client


def test_search_engine_init(mock_chroma, mock_embedding):
    """测试搜索引擎初始化"""
    engine = SearchEngine(
        chroma_path="./test_chroma",
        embedding_api_key="test-key"
    )
    assert engine is not None


def test_add_memory(mock_chroma, mock_embedding):
    """测试添加记忆到向量库"""
    engine = SearchEngine(
        chroma_path="./test_chroma",
        embedding_api_key="test-key"
    )
    memory = Memory(type=MemoryType.USER, content="测试内容")
    engine.add(memory)
    mock_chroma.add.assert_called_once()


def test_search(mock_chroma, mock_embedding):
    """测试语义搜索"""
    engine = SearchEngine(
        chroma_path="./test_chroma",
        embedding_api_key="test-key"
    )
    results = engine.search("测试查询", limit=5)
    assert len(results) > 0
    assert results[0]["id"] == "id1"
