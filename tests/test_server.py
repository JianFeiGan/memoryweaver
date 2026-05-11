import pytest
from unittest.mock import MagicMock, patch
from src.server import create_server


@pytest.fixture
def mock_deps():
    """Mock all heavy dependencies"""
    with (
        patch("src.server.Config") as MockConfig,
        patch("src.server.MemoryEngine") as MockEngine,
        patch("src.server.AutoExtractor") as MockExtractor,
    ):
        yield MockConfig, MockEngine, MockExtractor


@pytest.fixture
def server(mock_deps):
    """Create server with mocked dependencies"""
    return create_server(config_path="config.yaml")


def test_server_creation(mock_deps):
    """测试 MCP Server 创建"""
    server = create_server(config_path="config.yaml")
    assert server is not None


@pytest.mark.asyncio
async def test_server_tools_registered(server):
    """测试工具注册"""
    tools = await server.list_tools()
    tool_names = [t.name for t in tools]
    assert "save_memory" in tool_names
    assert "search_memory" in tool_names
    assert "list_memories" in tool_names
    assert "get_project_context" in tool_names
