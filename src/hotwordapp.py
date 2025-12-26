from src.datapacket import Event, EventType
from src.datasource import DataSource
from src.reporter import ResultCollector
from src.textprocessor import TextProcessor
from src.timewindow import TimeWindow

class HotWordApp:
    def __init__(self, file_path, mode="auto", window_size=600, default_window_size=True):
        self.source = DataSource(file_path)
        self.processor = TextProcessor()
        self.window = TimeWindow(window_size)
        self.reporter = ResultCollector()

        self.mode = mode
        self.default_window_size = default_window_size

    def run(self):
        last_query_time = -1

        while self.source.next_line_exist():
            if self.mode == "auto":
                event = self.source.get_next_event()

                if event is None:
                    continue
                
                # 自动模式下的词汇统计
                if event.event_type == EventType.DATA:
                    words = self.processor.process(event.content)
                    for word in words:
                        self.window.add_word(event.timestamp, word)

                # 自动模式下的查询记录
                elif event.event_type == EventType.QUERY:
                    topk_list = self.window.get_top_k(event.content)
                    self.reporter.record_result(event.timestamp, event.content, topk_list)
            
            elif self.mode == "interactive":
                cmd = input("\n输入下一个查询时刻：时 分 秒 格式如：'0 7 5' 若要退出查询请输入exit\n")
                if cmd.startswith("exit"):
                    break
                
                hour, min, second = cmd.split()
                query_time = int(hour) * 3600 + int(min) * 60 + int(second)

                while query_time < last_query_time:
                    print("查询错误：本次查询时刻不得早于上一次查询，请重新输入")
                    hour, min, second = input("\n输入下一个查询时刻：时 分 秒 格式如：'0 7 5'\n").split()
                    query_time = int(hour) * 3600 + int(min) * 60 + int(second)

                last_query_time = query_time
                topk = int(input("\n输入查询topK的值："))

                # 可以查询时设置窗口大小
                if self.default_window_size == False:
                    window_size = int(input("\n输入查询窗口的大小（单位为秒）："))
                    self.window.set_window_size(window_size)    

                query_succeded = False
                while self.source.next_line_exist():
                    event = self.source.get_next_event()
                    
                    if event is None:
                        continue

                    if event.event_type == EventType.DATA:
                        if event.timestamp > query_time:
                            topk_list = self.window.get_top_k(topk)
                            # 交互模式下特有的查询后终端显示结果
                            self.reporter.print_ascii_chart(query_time, topk, topk_list)
                            self.reporter.record_result(query_time, topk, topk_list)
                            query_succeded = True

                        words = self.processor.process(event.content)
                        for word in words:
                            self.window.add_word(event.timestamp, word)
                        
                        if query_succeded == True:
                            break
                
                # 最后一次查询时数据流已经全部读取
                if query_succeded == False:
                    topk_list = self.window.get_top_k(topk)
                    self.reporter.print_ascii_chart(query_time, topk, topk_list)
                    self.reporter.record_result(query_time, topk, topk_list)

        self.reporter.save_to_json()