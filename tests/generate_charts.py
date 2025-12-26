import matplotlib.pyplot as plt
import psutil
import os
import time
import random
from src.timewindow import TimeWindow

def get_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def run_experiment_once(data_count):
    """运行一次实验，返回 (耗时, 内存)"""
    window = TimeWindow(window_size=600)
    vocab = [f"w{i}" for i in range(2000)]
    
    # 准备数据
    data = []
    for i in range(data_count):
        data.append((i, random.choice(vocab)))
    
    start_t = time.time()
    
    # 模拟数据流
    for i, (ts, word) in enumerate(data):
        window.add_word(ts, word)
        # 模拟高频查询：每 500 次 add 查询一次
        if i % 500 == 0:
            window.get_top_k(10)
            
    end_t = time.time()
    mem = get_memory_mb()
    return (end_t - start_t), mem

def main():
    print(">>> 开始自动化性能测试与绘图...")
    
    # 定义不同的负载 (输入数据量)
    loads = [10000, 50000, 100000, 200000, 300000, 500000, 1000000]
    
    times = []
    throughputs = []
    memories = []
    
    for count in loads:
        print(f"Testing load: {count} events...", end="", flush=True)
        duration, mem = run_experiment_once(count)
        
        tps = count / duration # 吞吐量
        
        times.append(duration)
        throughputs.append(tps)
        memories.append(mem)
        print(f" Done. (TPS: {int(tps)})")

    # === 开始绘图 ===
    plt.figure(figsize=(15, 5))
    
    # 图1：处理耗时 (Latency Trend)
    plt.subplot(1, 3, 1)
    plt.plot(loads, times, marker='o', color='b')
    plt.title('Processing Time vs Load')
    plt.xlabel('Input Data Size (Events)')
    plt.ylabel('Total Time (s)')
    plt.grid(True)
    
    # 图2：吞吐量 (Throughput)
    plt.subplot(1, 3, 2)
    plt.plot(loads, throughputs, marker='s', color='g')
    plt.title('Throughput vs Load')
    plt.xlabel('Input Data Size (Events)')
    plt.ylabel('Throughput (Ops/sec)')
    plt.grid(True)
    
    # 图3：内存占用 (Memory Usage)
    plt.subplot(1, 3, 3)
    plt.plot(loads, memories, marker='^', color='r')
    plt.title('Memory Usage vs Load')
    plt.xlabel('Input Data Size (Events)')
    plt.ylabel('Memory (MB)')
    plt.grid(True)
    
    plt.tight_layout()
    
    output_img = "performance_report.png"
    plt.savefig(output_img)
    print(f"\n[Success] 图表已生成: {output_img}")
    print("请将此图片插入到你的作业文档中。")
    plt.show() # 如果在本地运行，会弹出窗口

if __name__ == "__main__":
    main()