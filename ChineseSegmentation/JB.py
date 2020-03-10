import jieba
import jieba.posseg as posseg
import jieba.analyse
from ChineseSegmentation import FileController as fc


# 基本分词，词性标注
def participle_text(text):
    stop_words = fc.get_stop_words()
    words = posseg.cut(text)
    result = ""
    i = 0
    for word in words:
        if word.word not in stop_words:
            if i > 0:
                result = result + " " + word.word
            else:
                result = result + word.word
            i = i + 1
    return result


# 分析文本，找出最大词频
def statistics_text_max():
    file_txt = fc.get_text()
    words = jieba.cut(file_txt)
    counts = {}

    for word in words:
        if len(word) == 1:  # 单个单词不考虑
            continue
        else:
            counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    for i in range(5):
        word, count = items[i]
        print("{0:<5}->{1:>5}".format(word, count))


# 添加词典
def add_dict(filename):
    jieba.load_userdict(filename)


# 添加单词
def add_words(words):
    for word in words:
        jieba.add_word(word)


# 建议单词合并
def suggest_freq(word):
    jieba.suggest_freq(word, True)


# 建议单词分割
def suggest_freq(word1, word2):
    jieba.suggest_freq((word1, word2), True)


# 基于 TF-IDF 算法的关键词抽取
def keywords_extraction_tf():
    file_txt = fc.get_text_2()
    keys = jieba.analyse.extract_tags(file_txt, topK=20, withWeight=True, allowPOS=())
    for word, weight in keys:
        print(word, weight)


# 基于 TF-IDF 算法的关键词抽取
def keywords_extraction_tt():
    file_txt = fc.get_text_2()
    keys = jieba.analyse.textrank(file_txt, topK=20, withWeight=True, allowPOS=("ns", "n", "vn", "v"))
    for word, weight in keys:
        print(word, weight)


# text = "我爱自然语言分析"
# # 全模式
# seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + " ".join(seg_list))
# # 标准模式
# seg_list = jieba.cut(text, cut_all=False)
# print("Default Mode: " + " ".join(seg_list))
# # 搜索模式
# seg_list = jieba.cut_for_search(text)
# print("Search Mode: " + " ".join(seg_list))/



