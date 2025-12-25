from collections import deque, defaultdict
import heapq

# 主逻辑，根据窗口大小更新词语并在查询时返回topK个词语
class TimeWindow:
    def __init__(self, window_size=600):
        self.window_size = window_size

        # 用双端队列维护当前词语列表
        self.window = deque()

        # 用字典模拟哈希表统计词语出现次数
        self.hash = defaultdict(int)
    
    def set_window_size(self, window_size):
        """用于外部改变窗口大小"""
        self.window_size = window_size
    
    def is_valid_time(self, timestamp):
        """判断时间戳是否合法"""
        if len(self.window) > 0:
            tail_time, _ = self.window[-1]

            if timestamp < tail_time:
                return False
            else:
                return True
        else:
            return True # 窗口为空时数据合法


    def del_expired_words(self, timestamp):
        """将过期词汇弹出窗口并在哈希表中删除"""
        while self.window:
            head_time, head_word = self.window[0]

            # 如果词语超出了窗口大小，将其在弹出队列并在哈希表中删除
            if timestamp - head_time > self.window_size:
                self.window.popleft()
                self.hash[head_word] -= 1
            
                # 如果词频已经减为0，将其从哈希表中删除
                if self.hash[head_word] == 0:
                    del self.hash[head_word]
            
            else:
                break
    
    def add_word(self, timestamp, word):
        """添加词汇"""
        # 每次添加新词前先将超出窗口时间的词语删除
        self.del_expired_words(timestamp)

        # 保证时间戳合法
        if self.is_valid_time(timestamp):
            self.window.append((timestamp, word))
            self.hash[word] += 1
    
    def get_top_k(self, k):
        """求出当前的topK热词"""
        return heapq.nsmallest(k, self.hash.items(), key=lambda x: (-x[1], x[0]))

