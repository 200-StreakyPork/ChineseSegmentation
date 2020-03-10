import chardet
import os
import codecs
import re


# 去除非中文字符
def clean_str(string):
    string = re.sub(r"[^\u4e00-\u9fff]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


# 打开文档
def get_text(filename):
    bytes = min(1000, os.path.getsize(filename))
    raw = open(filename, "rb").read(bytes)
    file_coding = chardet.detect(raw)["encoding"]
    # print(file_coding)
    file = open(filename, "r", encoding=file_coding, errors="ignore")
    txt = file.read()
    file.close()
    return txt


# 打开文档
# 弃用
def get_text_1(filename):
    file = codecs.open(filename, "r", "gbk", errors="ignore")
    txt = ""
    for line in file:
        line = clean_str(line)
        txt += line
    file.close()
    return txt


# 返回字典地址
def get_dict_path():
    return "dictionary/userdict"


def get_stop_words():
    stop_words = [line.strip() for line in open("dictionary/stop", encoding="UTF-8").readlines()]
    return stop_words
