from typing import Optional
import chromadb
import openai
from src.models import Memory


class SearchEngine:
    """混合搜索引擎 (语义 + 全文)"""

    def __init__(
        self,
        chroma_path: str,
        embedding_api_key: str,
        embedding_model: str = "text-embedding-3-small"
    ):
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="memories",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedding_client = openai.OpenAI(api_key=embedding_api_key)
        self.embedding_model = embedding_model

    def _get_embedding(self, text: str) -> list[float]:
        """获取文本的向量嵌入"""
        response = self.embedding_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def add(self, memory: Memory) -> None:
        """添加记忆到向量库"""
        embedding = self._get_embedding(memory.content)
        self.collection.add(
            ids=[memory.id],
            embeddings=[embedding],
            documents=[memory.content],
            metadatas=[{
                "type": memory.type.value,
                "source": memory.source or "",
                "project": (memory.metadata or {}).get("project", "")
            }]
        )

    def update(self, memory: Memory) -> None:
        """更新记忆向量"""
        embedding = self._get_embedding(memory.content)
        self.collection.update(
            ids=[memory.id],
            embeddings=[embedding],
            documents=[memory.content],
            metadatas=[{
                "type": memory.type.value,
                "source": memory.source or "",
                "project": (memory.metadata or {}).get("project", "")
            }]
        )

    def delete(self, id: str) -> None:
        """删除记忆向量"""
        self.collection.delete(ids=[id])

    def search(
        self,
        query: str,
        type_filter: Optional[str] = None,
        project: Optional[str] = None,
        limit: int = 10
    ) -> list[dict]:
        """语义搜索"""
        embedding = self._get_embedding(query)
        where = {}
        if type_filter:
            where["type"] = type_filter
        if project:
            where["project"] = project
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
            where=where if where else None
        )
        return [
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
            for i in range(len(results["ids"][0]))
        ]
