import os
import re
import yaml
from typing import Optional
from pydantic import BaseModel, Field


class StorageConfig(BaseModel):
    sqlite_path: str = "./data/memory.db"
    chroma_path: str = "./data/chroma"


class EmbeddingConfig(BaseModel):
    provider: str = "openai"
    api_key: str = ""
    model: str = "text-embedding-3-small"


class DeepSeekConfig(BaseModel):
    api_key: str = ""
    model: str = "deepseek-chat"


class ApiConfig(BaseModel):
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    deepseek: DeepSeekConfig = Field(default_factory=DeepSeekConfig)


class InjectionTarget(BaseModel):
    type: str
    path: str


class InjectionConfig(BaseModel):
    auto_inject: bool = True
    targets: list[InjectionTarget] = Field(default_factory=lambda: [
        InjectionTarget(type="cursor", path=".cursorrules"),
        InjectionTarget(type="claude", path=".claude/CLAUDE.md"),
        InjectionTarget(type="generic", path="AGENTS.md"),
    ])


class ExtractionConfig(BaseModel):
    auto_extract: bool = True
    trigger_after_turns: int = 10
    min_confidence: float = 0.7


class Config(BaseModel):
    storage: StorageConfig = Field(default_factory=StorageConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    injection: InjectionConfig = Field(default_factory=InjectionConfig)
    extraction: ExtractionConfig = Field(default_factory=ExtractionConfig)

    @classmethod
    def load(cls, path: str) -> "Config":
        """从 YAML 文件加载配置"""
        with open(path, 'r') as f:
            raw = f.read()
        # 替换环境变量
        raw = cls._substitute_env_vars(raw)
        data = yaml.safe_load(raw) or {}
        return cls(**data)

    @staticmethod
    def _substitute_env_vars(text: str) -> str:
        """替换 ${ENV_VAR} 格式的环境变量"""
        def replace(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))
        return re.sub(r'\$\{(\w+)\}', replace, text)
