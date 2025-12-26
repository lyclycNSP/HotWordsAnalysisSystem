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
import random
import os
import psutil
from src.timewindow import TimeWindow

# === 配置参数 ===
DATA_SIZE = 200000      # 测试的数据总量
WINDOW_SIZE = 600       # 滑动窗口大小
TOP_K = 10              # 每次查询 Top-10
QUERY_RATIO = 0.01      # 查询频率：每100条数据查询1次

def get_memory_mb():
    """获取当前进程内存占用(MB)"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def run_core_benchmark(data_count):
    """
    运行一次核心算法测试
    返回: (总耗时, 吞吐量OPS, 峰值内存MB)
    """
    window = TimeWindow(window_size=WINDOW_SIZE)
    
    # 预生成数据（在内存中），不计入算法耗时
    # 模拟 (时间戳, 单词)
    data_stream = []
    vocab = [f"word_{i}" for i in range(5000)] # 5000个唯一词汇
    
    current_time = 0
    for i in range(data_count):
        current_time += 1 # 模拟每秒一条
        word = random.choice(vocab)
        is_query = (i % int(1/QUERY_RATIO) == 0)
        data_stream.append((current_time, word, is_query))

    # 开始计时
    start_mem = get_memory_mb()
    start_time = time.time()
    
    query_count = 0
    
    for timestamp, word, is_query in data_stream:
        # 核心操作：添加词汇
        window.add_word(timestamp, word)
        
        # 核心操作：Top-K 查询
        if is_query:
            window.get_top_k(TOP_K)
            query_count += 1
            
    end_time = time.time()
    end_mem = get_memory_mb()
    
    duration = end_time - start_time
    throughput = data_count / duration if duration > 0 else 0
    
    print(f"--- Core Benchmark (N={data_count}) ---")
    print(f"耗时: {duration:.4f}s")
    print(f"吞吐: {throughput:.0f} ops/sec")
    print(f"内存: {end_mem:.2f} MB")
    
    return duration, throughput, end_mem

if __name__ == "__main__":
    print(">>> 正在进行纯算法核心测试...")
    run_core_benchmark(DATA_SIZE)