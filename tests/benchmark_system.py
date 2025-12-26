import sys
import os

# === 核心代码开始 ===
# 获取当前文件的目录 (test/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录 (test/ 的上一级)
project_root = os.path.dirname(current_dir)
# 将项目根目录加入到系统搜索路径中
sys.path.append(project_root)
# === 核心代码结束 ===

import time
import os
import psutil
import random
from src.hotwordapp import HotWordApp
from src.reporter import ResultCollector

# === 配置参数 ===
TEST_FILE = "data/system_bench.txt"
TOTAL_LINES = 50000     # 系统测试由于含分词，数量可以少一点
WINDOW_SIZE = 600

class SilentReporter(ResultCollector):
    """继承原有的Reporter，但是覆盖打印方法，不做任何输出，只做计算"""
    def print_ascii_chart(self, timestamp, k, topk_list):
        # 依然计算字符串宽度等逻辑，模拟真实计算负载，但禁止 print
        if not topk_list: return
        max_label_width = 0
        for word, _ in topk_list:
            w_width = self.get_display_width(str(word)) # 调用父类方法
            if w_width > max_label_width:
                max_label_width = w_width
        # 不执行 print

def generate_file(filepath, lines):
    """生成包含中文句子的测试文件"""
    print(f"正在生成测试文件: {filepath} ...")
    samples = ["人工智能发展迅速", "深度学习改变生活", "Python是最好的语言", "测试滑动窗口性能", "数据结构与算法"]
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        t = 0
        for i in range(lines):
            t += 1
            h, m, s = (t//3600)%24, (t%3600)//60, t%60
            content = random.choice(samples) + random.choice(samples)
            f.write(f"[{h:02d}:{m:02d}:{s:02d}] {content}\n")
            if i % 1000 == 0:
                f.write("[ACTION] QUERY K=5\n")

def get_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def run_system_benchmark():
    # 准备数据
    generate_file(TEST_FILE, TOTAL_LINES)
    
    # 初始化应用
    app = HotWordApp(TEST_FILE, mode="auto", window_size=WINDOW_SIZE)
    # 替换 reporter 为静音版，防止 IO 刷屏影响测试准确性
    app.reporter = SilentReporter()
    
    # 运行并计时
    print(">>> 系统全链路测试开始...")
    start_mem = get_memory_mb()
    start_time = time.time()
    
    app.run()
    
    end_time = time.time()
    end_mem = get_memory_mb()
    
    duration = end_time - start_time
    print(f"--- System Benchmark ---")
    print(f"处理行数: {TOTAL_LINES}")
    print(f"总耗时: {duration:.4f}s")
    print(f"系统吞吐: {TOTAL_LINES / duration:.2f} lines/sec")
    print(f"内存占用: {end_mem:.2f} MB")
    
    # 清理文件
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    
    return duration, end_mem

if __name__ == "__main__":
    run_system_benchmark()