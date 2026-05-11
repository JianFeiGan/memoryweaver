from datetime import datetime
from enum import Enum
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """记忆类型枚举"""
    USER = "user"
    PROJECT = "project"
    FEEDBACK = "feedback"
    REFERENCE = "reference"
    TEMPORARY = "temporary"


class Memory(BaseModel):
    """记忆数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MemoryType
    content: str
    metadata: Optional[dict] = None
    source: Optional[str] = None
    ttl: Optional[int] = None  # 生存时间(秒), None 表示永久
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    accessed_at: datetime = Field(default_factory=datetime.now)
    access_count: int = 0

    def to_dict(self) -> dict:
        """转换为字典"""
        return self.model_dump(mode="json")

    @classmethod
    def from_dict(cls, d: dict) -> "Memory":
        """从字典创建"""
        return cls(**d)
