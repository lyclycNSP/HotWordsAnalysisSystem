from src.datapacket import EventType, Event
import re

# DataSource类功能：
# 将txt文本流内容用正则表达式提取出（时间戳，文本/K的值，事件类型）的形式
class DataSource:
    def __init__(self, file_path):
        self.file_path = file_path
        self.gen = self.line_generator()
        self.not_finish = True
    
    # 使用生成器每次处理一行文本，不需要提前预读所有数据
    # 减轻内存压力
    def line_generator(self):
        """
        生成器: 使用yield 暂停函数执行，直到下一次被 next() 调用
        """
        try:
            with open(f"{self.file_path}", 'r', encoding="utf-8") as f:
                for line in f:
                    yield line
        
        except FileNotFoundError:
            print(f"错误：没有找到文件：{self.file_path}")
            self.not_finish = False
    
    def next_line_exist(self):
        """告诉主程序还有没有数据"""
        return self.not_finish
    
    def parse_timestamp(self, time_str):
        """将时间戳字符串 [H:MM:SS] 转换为秒数"""
        time_str = time_str.strip('[]')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def get_next_event(self):
        """获取下一条Event对象"""

        if self.not_finish == False:
            return None

        try:
            line = next(self.gen)

            line = line.strip()

            # 跳过空行
            if line:
                # 正则表达式处理字符串
                # 匹配数据行: [时间戳] 内容
                data_pattern = r'^\[(\d+:\d+:\d+)\]\s+(.+)$'
                # 匹配查询行: [ACTION] QUERY K=数字
                query_pattern = r'^\[ACTION\]\s+QUERY\s+K=(\d+)$'
                
                data_match = re.match(data_pattern, line)
                query_match = re.match(query_pattern, line)
                
                if data_match:
                    # 数据行
                    time_str = data_match.group(1)
                    content = data_match.group(2)
                    timestamp = self.parse_timestamp(time_str)
                    self.last_timestamp = timestamp  # 保存时间戳供查询使用
                    return Event(timestamp, content, EventType.DATA)
                
                elif query_match:
                    # 查询行
                    k_value = int(query_match.group(1))
                    # 使用上一条数据的时间戳，content为K值
                    return Event(self.last_timestamp, k_value, EventType.QUERY)
        
        except StopIteration:
            self.not_finish = False
            return None