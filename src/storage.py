from __future__ import annotations

import json
import sqlite_utils
from typing import Optional
from src.models import Memory, MemoryType


class SQLiteStorage:
    """SQLite 存储层"""

    def __init__(self, db_path: str):
        self.db = sqlite_utils.Database(db_path)
        self._init_tables()

    def _init_tables(self):
        """初始化数据库表"""
        if "memories" not in self.db.table_names():
            self.db["memories"].create({
                "id": str,
                "type": str,
                "content": str,
                "metadata": str,  # JSON
                "source": str,
                "ttl": int,
                "created_at": str,
                "updated_at": str,
                "accessed_at": str,
                "access_count": int,
            }, pk="id")
            self.db["memories"].create_index(["type"])
            self.db["memories"].create_index(["source"])
            # 启用全文搜索 (create_triggers=True 保证插入/更新/删除自动同步)
            self.db["memories"].enable_fts(["content", "metadata"], create_triggers=True)

    def save(self, memory: Memory) -> Memory:
        """保存记忆"""
        data = memory.to_dict()
        data["metadata"] = json.dumps(data.get("metadata") or {})
        self.db["memories"].upsert(data, pk="id")
        return memory

    def get(self, id: str) -> Optional[Memory]:
        """获取记忆"""
        try:
            row = self.db["memories"].get(id)
            if row:
                d = dict(row)
                d["metadata"] = json.loads(d.get("metadata") or "{}") or None
                return Memory.from_dict(d)
        except Exception:
            pass
        return None

    def list(
        self,
        type_filter: Optional[MemoryType] = None,
        source: Optional[str] = None,
        limit: int = 50
    ) -> list[Memory]:
        """列出记忆"""
        where = []
        params = []
        if type_filter:
            where.append("type = ?")
            params.append(type_filter.value)
        if source:
            where.append("source = ?")
            params.append(source)
        where_str = " AND ".join(where) if where else None
        results = []
        for row in self.db["memories"].rows_where(
            where_str, params, order_by="created_at desc", limit=limit
        ):
            d = dict(row)
            d["metadata"] = json.loads(d.get("metadata") or "{}") or None
            results.append(Memory.from_dict(d))
        return results

    def delete(self, id: str) -> bool:
        """删除记忆"""
        try:
            self.db["memories"].delete(id)
            return True
        except Exception:
            return False

    def search_text(self, query: str, limit: int = 10) -> list[Memory]:
        """全文搜索"""
        results = []
        # Wrap in quotes for FTS5 phrase matching to handle special chars like "."
        fts_query = f'"{query}"'
        try:
            for row in list(self.db["memories"].search(fts_query))[:limit]:
                d = dict(row)
                d["metadata"] = json.loads(d.get("metadata") or "{}") or None
                results.append(Memory.from_dict(d))
        except Exception:
            pass
        return results
