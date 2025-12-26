# 基于滑动窗口的热词统计与分析系统
## 项目简介
本项目实现了一个针对流式文本数据的实时热词统计系统。基于**双端队列、哈希表和小根堆**的数据结构，实现了 `O(1)` 复杂度的实时词频更新与 `O(M*log K)` 复杂度（M为哈希表中不同词汇数）的 Top-K 查询。系统支持自动读入文本流和命令行交互，并基于 Web 进行可视化展示。

---

## 环境要求
+ **操作系统**: Windows /  Linux
+ **Python 版本**: Python 3.10+
+ **依赖库**: 
    - **Jieba**: 用于中文分词。
        * 版本：0.42.1
        * 许可证：MIT License
    - **Streamlit** : 用于构建 Web 界面。
        * 版本：1.52.2
        * 许可证：Apache 2.0
    - **altair** : 用于实现多彩柱状图
        * 版本：6.0.0
        * 许可证：BSD 3-Clause
    - **pytest**: 用于进行单元测试
        * 版本：9.0.2
        * 许可证：MIT

---

## 快速开始
### 克隆仓库或解压文件
### 进入 data 文件夹，修改 input_auto.txt 或 input_interactive.txt
+ **input_auto.txt** 的输入数据需按照 `[H:MM:SS] <文本数据>` 的格式提供，每行一条文本数据。在需要查询的位置插入一行`[ACTION] QUERY K=<整数>`。如：

```plain
[0:04:27] 你们三兄弟长的一点都不一样
[ACTION] QUERY K=6
[0:04:27] 诸葛瑾确实是神级管家！其他能力就一般了
```

+ **input_interactive.txt** 的输入的文本数据同样按照 `[H:MM:SS] <文本数据>` 的格式提供，每行一条文本数据。但不再需要在文件中提供 `[ACTION] QUERY K=<整数>` 指令。用户可以稍后在终端交互窗口处手动输入时间点和窗口大小进行查询

### 运行 run_auto.bat 或 run_interactive.bat（涵盖python依赖库的安装）
注：linux环境需安装python依赖库：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

##  运行模式 
### 模式一：自动模式（auto）
```bash
# 进入data文件夹修改input_auto.txt
cd data
code input_auto.txt

# 运行代码，需要在命令后加入指定模式和默认窗口大小（单位秒）
python main.py --mode auto -w 600
```

### 模式二：交互模式（interactive）
```bash
# 进入data文件夹修改input_interactive.txt
cd data
code input_interactive.txt

# 运行代码，需要在命令后加入指定模式，不需要指定默认窗口大小
python main.py --mode auto
```

_注：启动后会自动打开浏览器，若未打开请访问终端显示的 Local URL (如 _[http://localhost:8501](http://localhost:8501)_)_

## 运行单元测试
验证核心算法的正确性：
### 方式一：运行test.bat单元测试脚本

### 方式二：命令行
```bash
venv\Scripts\activate.bat # cmd
.\venv\Scripts\activate # powershell
python -m pytest
```

## 项目目录结构
```latex
HotWordsAnalysisSystem/
├── data/
│   ├── input_auto.txt            # 输入数据源
│   ├── input_interactive.txt     
│   ├── stopwords.txt             # 停用词表
│   └── results.json              # 查询结果保存位置
├── docs                          # 文档报告
├── src/                          # 实现源码
│   ├── __init__.py 
│   ├── datapacket.py         
│   ├── datasource.py       
│   ├── hotwordapp.py       
│   ├── reporter.py       
│   ├── textprocessor.py       
│   ├── timewindow.py   
│   └── visualize.py    
├── tests/                       # 性能测试与单元测试文件
│   ├── __init__.py 
│   ├── benchmark_core.py
│   ├── benchmark_system.py
│   ├── generate_charts.py
│   ├── test_processor.py
│   └── test_timewindow.py         
├── main.py                      # 主程序
├── performance_report.png       # 性能测试图表                
├── requirements.txt             # 依赖列表
├── run_auto.bat                 # 自动模式运行脚本
├── run_interactive.bat          # 交互模式运行脚本
├── test.bat                     # 单元测试运行脚本
└── README.md                    # 操作说明
```

## 特性说明
+ **文本清洗**: 集成 Jieba 分词，支持停用词过滤与自定义词典。
+ **滑动时间窗口**：采用高效的时间窗口算法，实时追踪指定时间段内的词频变化
+ **TopK 排行** ：高效的词频统计和排序算法，快速获取指定数量的高频词汇
+ **可视化**: 提供时间轴滑块，可交互式查看不同时刻的热词分布趋势。
+ **分层架构设计** ：采用模块化设计，时间窗口管理器、词频排名管理器各司其职
+ **跨平台支持**：支持 Linux、Windows 等多平台编译运行
+ **测试保障**：使用 pytest 测试框架，确保代码质量和稳定性



