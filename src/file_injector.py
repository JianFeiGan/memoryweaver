import os


class FileInjector:
    """文件注入模块"""

    def __init__(self, project_path: str = "."):
        self.project_path = project_path

    def generate(self, target: str, context: str) -> dict:
        """生成注入文件内容"""
        generators = {
            "cursor": self._generate_cursor,
            "claude": self._generate_claude,
            "generic": self._generate_generic,
        }
        generator = generators.get(target, self._generate_generic)
        return generator(context)

    def write(self, result: dict) -> str:
        """写入文件"""
        file_path = os.path.join(self.project_path, result["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result["content"])
        return file_path

    def _generate_cursor(self, context: str) -> dict:
        """生成 .cursorrules"""
        content = f"""# Cursor Rules (自动生成 by MemoryWeaver)

{context}
"""
        return {"path": ".cursorrules", "content": content}

    def _generate_claude(self, context: str) -> dict:
        """生成 .claude/CLAUDE.md"""
        content = f"""# CLAUDE.md (自动生成 by MemoryWeaver)

{context}
"""
        return {"path": ".claude/CLAUDE.md", "content": content}

    def _generate_generic(self, context: str) -> dict:
        """生成 AGENTS.md"""
        content = f"""# Agent Context (自动生成 by MemoryWeaver)

{context}
"""
        return {"path": "AGENTS.md", "content": content}
