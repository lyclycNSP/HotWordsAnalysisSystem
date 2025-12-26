import jieba

# TextProcessor类将每一行的文本拆分成独立词语提供给后续逻辑处理
class TextProcessor:
    def __init__(self):
        self.stopwords = set()
        # 读取停用词表
        with open("data/stopwords.txt", "r", encoding="utf-8") as f:
            for line in f:
                self.stopwords.add(line.strip())

    def process(self, text):
        """将句子切分成词语"""
        words = jieba.lcut(text)
        # 过滤停顿词后返回结果
        return [w for w in words if w not in self.stopwords and len(w) > 1 and not w.isspace()]