#encoding=utf-8
import jieba

jieba.set_dictionary('extra_dict/dict.txt.big')
jieba.load_userdict('extra_dict/userdict.txt')
content = open('lyric.txt', 'rb').read()
seg_list = jieba.cut(content)
print ", ".join(seg_list)