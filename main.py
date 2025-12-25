from src.datapacket import Event, EventType
from src.datasource import DataSource
from src.textprocessor import TextProcessor
from src.timewindow import TimeWindow
from src.reporter import ResultCollector
from src.hotwordapp import HotWordApp
import os

if __name__ == "__main__":
    import argparse
    import subprocess

    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["auto", "interactive"], default="auto", help="运行模式")

    parser.add_argument("--window_size", "-w", type=int, required=False, help="滑动窗口大小(秒)。Auto模式下必填，Interactive模式下选填(默认600)")
    

    args = parser.parse_args()

    final_window_size = 600

    if args.mode == "auto":
        if args.window_size is None:
            parser.error("错误：在 'auto' 模式下，必须提供 --window_size / -w 参数。")
        else:
            final_window_size = args.window_size
        
        print(f"自动查询模式启动，已设置默认滑动窗口大小为{final_window_size}\n")
        app = HotWordApp("data/input_auto.txt", mode=args.mode, window_size=final_window_size)
    
    else:
        print(f"交互模式启动，是否要设置默认滑动窗口大小？")
        cmd = input("\n 输入'yes 600' 设置默认滑动窗口大小为600秒, 'no' 不设置默认窗口大小，后续可以手动输入查询结果:")
        default_window_size = False

        if cmd.startswith('yes'):
            try:
                final_window_size = int(cmd.split()[1])
                default_window_size = True
            except:
                print("指令错误，格式如: yes 600")

        app = HotWordApp("data/input_interactive.txt", mode=args.mode, window_size=final_window_size, default_window_size=default_window_size)
    
    app.run()
    
    print("\n" + "="*50)
    print("[提示] 正在启动可视化页面...")
    print("[提示] 如果浏览器没有自动弹出，请手动访问: http://localhost:8501")
    print("="*50 + "\n")

    visual_script = os.path.join("src", "visualize.py") 
    
    if os.path.exists(visual_script):
        # 相当于在命令行中输入：streamlit run src/app_viz.py
        subprocess.run(["streamlit", "run", visual_script])
    else:
        print(f"Error: 找不到可视化脚本 {visual_script}")
