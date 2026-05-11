from mcp.server.fastmcp import FastMCP
import json
from src.config import Config
from src.memory_engine import MemoryEngine
from src.auto_extractor import AutoExtractor
from src.models import MemoryType


def create_server(config_path: str = "config.yaml") -> FastMCP:
    """创建 MCP Server"""
    config = Config.load(config_path)
    engine = MemoryEngine(
        db_path=config.storage.sqlite_path,
        chroma_path=config.storage.chroma_path,
        embedding_api_key=config.api.embedding.api_key,
        embedding_model=config.api.embedding.model,
    )
    extractor = AutoExtractor(
        api_key=config.api.deepseek.api_key,
        model=config.api.deepseek.model,
    )
    server = FastMCP("memoryweaver")

    @server.tool()
    async def save_memory(
        type: str,
        content: str,
        metadata: dict = None,
        source: str = None,
    ) -> str:
        """保存记忆"""
        memory = engine.save(
            type=MemoryType(type),
            content=content,
            metadata=metadata,
            source=source,
        )
        return json.dumps(memory.to_dict(), ensure_ascii=False)

    @server.tool()
    async def search_memory(
        query: str,
        type: str = None,
        project: str = None,
        limit: int = 10,
    ) -> str:
        """搜索记忆"""
        results = engine.search(
            query, type_filter=type, project=project, limit=limit
        )
        return json.dumps(results, ensure_ascii=False)

    @server.tool()
    async def list_memories(
        type: str = None,
        project: str = None,
        limit: int = 50,
    ) -> str:
        """列出记忆"""
        type_filter = MemoryType(type) if type else None
        memories = engine.list(type_filter=type_filter, limit=limit)
        return json.dumps(
            [m.to_dict() for m in memories], ensure_ascii=False
        )

    @server.tool()
    async def get_project_context(
        project: str = None,
        include_personal: bool = True,
    ) -> str:
        """获取项目上下文"""
        return engine.get_project_context(project, include_personal)

    @server.tool()
    async def extract_from_conversation(
        conversation: str,
        project: str = None,
    ) -> str:
        """从对话中提取记忆"""
        memories = extractor.extract(conversation, project)
        for memory in memories:
            engine.save(
                type=memory.type,
                content=memory.content,
                metadata=memory.metadata,
                source="auto-extractor",
            )
        return json.dumps(
            [m.to_dict() for m in memories], ensure_ascii=False
        )

    return server


def main():
    """启动 MCP Server"""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
