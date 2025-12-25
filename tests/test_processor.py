import pytest
from src.textprocessor import TextProcessor

@pytest.fixture
def processor():
    """创建一个分词处理的实例供测试使用"""
    return TextProcessor()

def test_process(processor):
    text = "测试一行文本的分词结果。"
    words = processor.process(text)

    assert "测试" in words
    assert "文本" in words
    assert "分词" in words