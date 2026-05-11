from __future__ import annotations

from typing import Optional
from src.models import Memory, MemoryType
from src.storage import SQLiteStorage
from src.search_engine import SearchEngine


class MemoryEngine:
    """核心记忆引擎"""

    def __init__(
        self,
        db_path: str,
        chroma_path: str,
        embedding_api_key: str,
        embedding_model: str = "text-embedding-3-small"
    ):
        self.storage = SQLiteStorage(db_path)
        self.search_engine = SearchEngine(
            chroma_path=chroma_path,
            embedding_api_key=embedding_api_key,
            embedding_model=embedding_model
        )

    def save(
        self,
        type: MemoryType,
        content: str,
        metadata: Optional[dict] = None,
        source: Optional[str] = None,
        ttl: Optional[int] = None
    ) -> Memory:
        """保存记忆"""
        memory = Memory(
            type=type,
            content=content,
            metadata=metadata,
            source=source,
            ttl=ttl
        )
        self.storage.save(memory)
        self.search_engine.add(memory)
        return memory

    def get(self, id: str) -> Optional[Memory]:
        """获取记忆"""
        return self.storage.get(id)

    def list(
        self,
        type_filter: Optional[MemoryType] = None,
        project: Optional[str] = None,
        limit: int = 50
    ) -> list[Memory]:
        """列出记忆"""
        return self.storage.list(type_filter=type_filter, limit=limit)

    def update(
        self,
        id: str,
        content: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> Optional[Memory]:
        """更新记忆"""
        memory = self.storage.get(id)
        if not memory:
            return None
        if content:
            memory.content = content
        if metadata:
            memory.metadata = metadata
        from datetime import datetime
        memory.updated_at = datetime.now()
        self.storage.save(memory)
        self.search_engine.update(memory)
        return memory

    def delete(self, id: str) -> bool:
        """删除记忆"""
        self.search_engine.delete(id)
        return self.storage.delete(id)

    def search(
        self,
        query: str,
        type_filter: Optional[str] = None,
        project: Optional[str] = None,
        limit: int = 10
    ) -> list[dict]:
        """搜索记忆 (语义 + 全文)"""
        # 语义搜索
        semantic_results = self.search_engine.search(
            query=query,
            type_filter=type_filter,
            project=project,
            limit=limit
        )
        # 全文搜索
        text_results = self.storage.search_text(query, limit=limit)
        # 合并去重
        seen_ids = set()
        combined = []
        for r in semantic_results:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                combined.append(r)
        for r in text_results:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                combined.append({"id": r.id, "content": r.content, "metadata": r.to_dict()})
        return combined[:limit]

    def get_project_context(
        self,
        project: Optional[str] = None,
        include_personal: bool = True
    ) -> str:
        """获取项目上下文"""
        sections = []
        # 项目记忆
        project_memories = self.storage.list(type_filter=MemoryType.PROJECT, limit=20)
        if project:
            project_memories = [m for m in project_memories if (m.metadata or {}).get("project") == project]
        if project_memories:
            sections.append("## 项目信息\n" + "\n".join(f"- {m.content}" for m in project_memories))
        # 个人记忆
        if include_personal:
            user_memories = self.storage.list(type_filter=MemoryType.USER, limit=10)
            if user_memories:
                sections.append("## 开发者偏好\n" + "\n".join(f"- {m.content}" for m in user_memories))
        # 反馈记忆
        feedback_memories = self.storage.list(type_filter=MemoryType.FEEDBACK, limit=10)
        if feedback_memories:
            sections.append("## 行为指导\n" + "\n".join(f"- {m.content}" for m in feedback_memories))
        return "\n\n".join(sections) if sections else "暂无相关记忆"
