import pytest
import os
import tempfile
import yaml
from src.config import Config


def test_config_load_from_file():
    """测试从文件加载配置"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            "storage": {"sqlite_path": "/tmp/test.db"},
            "api": {"deepseek": {"api_key": "test-key"}}
        }, f)
        f.flush()
        config = Config.load(f.name)
        assert config.storage.sqlite_path == "/tmp/test.db"
        assert config.api.deepseek.api_key == "test-key"
        os.unlink(f.name)


def test_config_env_var_substitution():
    """测试环境变量替换"""
    os.environ["TEST_API_KEY"] = "env-key-value"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            "api": {"deepseek": {"api_key": "${TEST_API_KEY}"}}
        }, f)
        f.flush()
        config = Config.load(f.name)
        assert config.api.deepseek.api_key == "env-key-value"
        os.unlink(f.name)
        del os.environ["TEST_API_KEY"]


def test_config_defaults():
    """测试默认值"""
    config = Config()
    assert config.storage.sqlite_path == "./data/memory.db"
    assert config.extraction.min_confidence == 0.7
