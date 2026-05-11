```markdown
# memoryweaver Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `memoryweaver` Python codebase. You'll learn about file naming, import/export styles, commit message conventions, and how to write and organize tests. This guide is designed to help contributors maintain consistency and quality across the project.

## Coding Conventions

### File Naming
- **Style:** Snake case  
  **Example:**  
  ```python
  memory_manager.py
  data_utils.py
  ```

### Import Style
- **Style:** Relative imports are used within the project.  
  **Example:**  
  ```python
  from .memory_manager import MemoryManager
  from .utils import process_data
  ```

### Export Style
- **Style:** Named exports (explicitly listing what is exported).  
  **Example:**  
  ```python
  __all__ = ["MemoryManager", "process_data"]
  ```

### Commit Messages
- **Convention:** Conventional commits  
- **Prefixes:** `feat`, `test`  
- **Format Example:**  
  ```
  feat: add memory serialization logic
  test: add unit tests for memory manager
  ```

## Workflows

_No automated workflows detected in this repository._

## Testing Patterns

- **Framework:** Unknown (no standard Python test framework detected)
- **File Pattern:** Test files use the `.test.ts` suffix, which is typical for TypeScript, not Python. This suggests either a mixed-language repository or a misconfiguration.
- **Example Test File Name:**  
  ```
  memory_manager.test.ts
  ```
- **Note:** If writing new Python tests, follow the naming convention and place tests in files ending with `.test.ts` unless otherwise specified by the team.

## Commands
| Command | Purpose |
|---------|---------|
| /commit-convention | Show commit message guidelines |
| /file-naming       | Show file naming rules         |
| /import-style      | Show import style guidelines   |
| /export-style      | Show export style guidelines   |
| /testing           | Show how to write and locate tests |
```
