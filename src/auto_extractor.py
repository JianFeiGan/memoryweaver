import json
import openai
from typing import Optional
from src.models import Memory, MemoryType


EXTRACT_PROMPT = """
分析以下对话，提取值得长期保存的信息。

对话内容：
{conversation}

请提取以下类型的记忆（JSON 数组格式）：
[
  {{"type": "user", "content": "用户偏好描述", "confidence": 0.9}},
  {{"type": "project", "content": "项目相关信息", "confidence": 0.8}},
  {{"type": "feedback", "content": "行为指导", "confidence": 0.7}},
  {{"type": "reference", "content": "外部资源引用", "confidence": 0.8}}
]

只提取明确陈述的信息，不要推测。confidence 表示置信度 (0-1)。
返回纯 JSON，不要包含其他文字。"""


class AutoExtractor:
    """自动提炼模块"""

    def __init__(self, api_key: str, model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com"):
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def extract(
        self,
        conversation: str,
        project: Optional[str] = None,
        min_confidence: float = 0.7
    ) -> list[Memory]:
        """从对话中提取记忆"""
        prompt = EXTRACT_PROMPT.format(conversation=conversation)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        try:
            items = json.loads(content)
        except json.JSONDecodeError:
            return []
        memories = []
        for item in items:
            if item.get("confidence", 0) < min_confidence:
                continue
            memory_type = MemoryType(item["type"])
            metadata = {}
            if project:
                metadata["project"] = project
            memory = Memory(
                type=memory_type,
                content=item["content"],
                metadata=metadata if metadata else None,
                source="auto-extractor"
            )
            memories.append(memory)
        return memories
