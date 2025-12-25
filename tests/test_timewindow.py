import pytest
from src.timewindow import TimeWindow

@pytest.fixture
def window():
    """创建一个窗口大小为 10秒 的实例供测试使用"""
    return TimeWindow(10)

def test_expired_words(window):
    """
    测试过期数据是否被正确淘汰
    以及外部调用方法是否能正确改变窗口大小
    """
    # 窗口大小是 10s
    # t=1s, "苹果" 出现
    window.add_word(1, "苹果")
    
    # t=5s, "香蕉" 出现
    window.add_word(5, "香蕉")
    
    # t=12s, "西瓜" 出现
    # 此时，1s 的 "苹果" 应该过期
    # 5s 的 "香蕉" 应该还在
    window.add_word(12, "西瓜")

    # 获取 Top-3
    top_list = window.get_top_k(3)
    words = [item[0] for item in top_list]
    
    assert "苹果" not in words, "错误：苹果 应该已经过期被移除了"
    assert "香蕉" in words, "错误：香蕉 应该还在窗口内"
    assert "西瓜" in words, "错误：西瓜 应该还在窗口内"
    
    # 验证计数
    counts = dict(top_list)
    assert counts["香蕉"] == 1, "错误：香蕉 出现的次数应该是1"
    
    # 验证改变窗口大小的功能
    window.set_window_size(5)
    window.add_word(18, "葡萄")

    top_list = window.get_top_k(2)
    words = [item[0] for item in top_list]

    assert "西瓜" not in words, "错误：西瓜 应该已经过期被移除了"

def test_top_k_sorting(window):
    """测试 Top-K 排序是否正确"""

    window.add_word(1, "A")
    window.add_word(1, "B")
    window.add_word(2, "A")
    window.add_word(2, "B")
    window.add_word(2, "C")
    window.add_word(3, "C") 
    window.add_word(3, "B")
    
    # A=2, B=3, C=2
    # 按照出现次数降序排序，若出现次数相同则按字典序升序排序
    # 结果应该是 [(B, 3), (A, 2), (C, 2)]
    top_3 = window.get_top_k(3)
    
    assert top_3[0][0] == "B"
    assert top_3[0][1] == 3
    assert top_3[1][0] == 'A'
    assert top_3[2][0] == "C"
    assert len(top_3) == 3