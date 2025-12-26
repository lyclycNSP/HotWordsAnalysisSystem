from src.datapacket import Event, EventType
import os
import json
import unicodedata

# 接收查询结果，格式化输出到控制台
# 或者保存为 json 给 streamlit 用
class ResultCollector:
    def __init__(self):
        self.snapshots = []
    
    def record_result(self, timestamp, k, topk_list):
        """
        将每次查询的信息记录在一个列表中便于最后streamlit显示
        """
        if not topk_list:
            print("No data.")
            return
        
        content ={}
        content["time"] = self.format_time(timestamp)
        content["k"] = k
        content["data"] = dict(topk_list)

        self.snapshots.append(content)

    def get_display_width(self, text):
        """
        计算字符串的视觉显示宽度
        汉字/全角符号 = 2 width
        英文/数字/半角 = 1 width
        """
        width = 0
        for char in text:
            # east_asian_width 返回 'W'(Wide), 'F'(Full-width) 代表全角
            # 'A'(Ambiguous) 在很多终端下也是全角
            if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
                width += 2
            else:
                width += 1
        return width
    
    def print_ascii_chart(self, timestamp, k, topk_list):
        show_time = self.format_time(timestamp)
        
        print(f"\n=== [Time: {show_time}] ===")
        print(f"=== Top {k} Hot Words ===")

        if not topk_list:
            print("No data.")
            print("==========================================\n")
            return

        # 计算当前这一批词里，最长的那个词的视觉宽度是多少
        # 这样可以保证无论是2个字的词还是10个字的词，自适应对齐
        max_label_width = 0
        for word, _ in topk_list:
            w_width = self.get_display_width(str(word))
            if w_width > max_label_width:
                max_label_width = w_width
        
        # 增加一点缓冲空间，比如最少给 8 的宽度，避免太窄
        max_label_width = max(max_label_width, 8)

        # 准备画柱状图的参数
        max_count = topk_list[0][1]
        max_bar_len = 50 

        for word, count in topk_list:
            # 计算当前词的宽度
            current_width = self.get_display_width(str(word))
            
            # 补的空格数 = 目标总宽度 - 当前词的视觉宽度
            padding_len = max_label_width - current_width
            padding = " " * padding_len
            
            # 计算柱子长度
            if max_count > 0:
                bar_len = int((count / max_count) * max_bar_len)
            else:
                bar_len = 0
            bar_str = '█' * bar_len

            # 拼接打印
            # word + padding 组成了等长的左侧区域
            print(f"{word}{padding} | {bar_str} ({count})")
            
        print("==========================================\n")
    
    def save_to_json(self, filepath="data/results.json"):
        # 确保目录存在，如果没有 data 文件夹，将自动创建
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.snapshots, f, ensure_ascii=False, indent=2)
                print(f"\n[Success] 结果已保存至: {filepath}")
        except Exception as e:
            print(f"[Error] 保存 json 失败: {e}")

    def format_time(self, seconds):
        """辅助函数：把秒变成 00:00:00"""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
