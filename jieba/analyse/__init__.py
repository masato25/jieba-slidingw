# -*- encoding: utf-8 -*-
import jieba
import jieba.posseg
import os
from operator import itemgetter
import re
try:
    from analyzer import ChineseAnalyzer
except ImportError:
    pass
from textrank import textrank
import logging
import codecs

logging.basicConfig(file="./debug.log",level=logging.INFO)
_curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
abs_path = os.path.join(_curpath, "idf.txt")

STOP_WORDS = set((
    "the","of","is","and","to","in","that","we","for","an","are","by","be","as","on",
    "with","can","if","from","which","you","it","this","then","at","have","all","not",
    "one","has","or","that",u"的",u"和",".",",",u"［",u"］","<",">",":",";","^","*","{","}",u".",u",",
    "，",u"『",u"』",u"●",u"，",u"。",u"「",u"」",u"~",u"】",u"【",u"：",u"？",u"！",u"(",
    u")",u"、","%",u"～",u"“",u"”","/",u"《",u"》","=","[","]",'"',u"（",u"）",":","　",u"　",u"．",
    u"：","&",u"／","　","-","!","?"
))

NOT_IN_BRFORE = set((
    "%","+",u"+"
))

class IDFLoader:
    def __init__(self):
        self.path = ""
        self.idf_freq = {}
        self.median_idf = 0.0

    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            content = open(new_idf_path, 'rb').read().decode('utf-8')
            idf_freq = {}
            lines = content.rstrip('\n').split('\n')
            for line in lines:
                word, freq = line.split(' ')
                idf_freq[word] = float(freq)
            median_idf = sorted(idf_freq.values())[len(idf_freq)//2]
            self.idf_freq = idf_freq
            self.median_idf = median_idf
            self.path = new_idf_path

    def get_idf(self):
        return self.idf_freq, self.median_idf

idf_loader = IDFLoader()
idf_loader.set_new_path(abs_path)

def set_idf_path(idf_path):
    new_abs_path = os.path.normpath(os.path.join(os.getcwd(), idf_path))
    if not os.path.exists(new_abs_path):
        raise Exception("jieba: path does not exist: " + new_abs_path)
    idf_loader.set_new_path(new_abs_path)

def set_stop_words(stop_words_path):
    global STOP_WORDS
    abs_path = os.path.normpath(os.path.join(os.getcwd(), stop_words_path))
    if not os.path.exists(abs_path):
        raise Exception("jieba: path does not exist: " + abs_path)
    content = open(abs_path,'rb').read().decode('utf-8')
    lines = content.replace("\r", "").split('\n')
    for line in lines:
        STOP_WORDS.add(line)

def extract_tags(sentence, topK=20, withWeight=False, allowPOS=[]):
    """
    Extract keywords from sentence using TF-IDF algorithm.
    Parameter:
        - topK: return how many top keywords. `None` for all possible words.
        - withWeight: if True, return a list of (word, weight);
                      if False, return a list of words.
        - allowPOS: the allowed POS list eg. ['ns', 'n', 'vn', 'v','nr'].
                    if the POS of w is not in this list,it will be filtered.
    """
    global STOP_WORDS, idf_loader

    idf_freq, median_idf = idf_loader.get_idf()

    if allowPOS:
        allowPOS = frozenset(allowPOS)
        words = jieba.posseg.cut(sentence)
    else:
        words = jieba.cut(sentence)
    freq = {}
    for w in words:
        if allowPOS:
            if w.flag not in allowPOS:
                continue
            else:
                w = w.word
        if len(w.strip()) < 2 or w.lower() in STOP_WORDS:
            continue
        freq[w] = freq.get(w, 0.0) + 1.0
    total = sum(freq.values())
    for k in freq:
        freq[k] *= idf_freq.get(k, median_idf) / total

    if withWeight:
        tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
    else:
        tags = sorted(freq, key=freq.__getitem__, reverse=True)
    if topK:
        return tags[:topK]
    else:
        return tags


def extract_tags_custom(sentence, topK=20, withWeight=False,detectedwdsavepath=None):
    global STOP_WORDS, idf_loader, ff, NOT_IN_BRFORE

    # for save new words
    ff = open(detectedwdsavepath, 'aw+')

    idf_freq, median_idf = idf_loader.get_idf()
    #get cut words result
    words = jieba.cut(sentence,cut_all=False)
    #for save templete data
    freq,words_pool = {},[]

    for w in words:
        words_pool.append(w)
        if len(w.strip()) < 2 or w in STOP_WORDS:
            continue
        freq[w] = freq.get(w, 0.0) + 1.0

    tags = sorted(freq, key=freq.__getitem__, reverse=True)
    topk_wd = [k for k in tags[:topK]]
    findex = {}
    counter = 0
    #get the index of the topK words
    for w in words_pool:
        if w in topk_wd:
            if not findex.has_key(w):
                findex[w] = [counter]
            else:
                findex[w] = findex[w] + [counter]
        counter += 1
    #get cut result number of words
    totalllen = len(words_pool)
    new_topK = findex.copy()
    #for each check the topK words,sliding windows trace for words
    for k,v in findex.iteritems():
        fixwarrboth = []
        fixwarrbefore = []
        fixwarrafter = []
        #get the topK words indexes
        for indv in v:
            #if the before hit the beginning & endding. I will treat it as no need sliding check
            if indv - 1 < 0 or indv + 2 > totalllen:
                #init the fixwarrboth == nil , will tell the next step , you don't need check it.
                fixwarrboth = []
                break
            else:
                #get the pervious words of the topK
                beforeone = re.sub(r"(^\s+|\s$)","",words_pool[indv-1])
                if not beforeone in STOP_WORDS and not beforeone in NOT_IN_BRFORE:
                    fixwarrbefore.append(beforeone + words_pool[indv])
                #get the next words of the topK
                afterone = re.sub(r"(^\s+|\s$)","",words_pool[indv+1])
                if not afterone in STOP_WORDS:
                    fixwarrafter.append(words_pool[indv] + afterone)
                if not beforeone in STOP_WORDS and not afterone in STOP_WORDS:
                    fixwarrboth.append(beforeone + words_pool[indv] + afterone)


        """
        *need fix, when the fixwarrboth is true. need stop the before & adter comparetion
        """
        logicrun_flag = False
        for fixw in  [fixwarrboth,fixwarrbefore,fixwarrafter]:
            #print ",".join(fixw)
            if len(fixw) < 2 or logicrun_flag:
                break
            cflag = False
            #get the first one
            currentwords = fixw[0]
            #if all of the words are the same.means we need the sliding the words to the new words
            for cc in fixw:
                if currentwords == cc:
                    cflag = True
                else:
                    cflag = False
                    break
            if cflag:
                #remove the space
                currentwords = re.sub(r"(^\s+|\s+$)", "", currentwords)
                #if the the currentwords != topK orginal words.
                if currentwords != k:
                    #set the new words into the topK to the result set
                    new_topK[currentwords] = v
                    logicrun_flag = True
                    if new_topK.has_key(k):
                        del new_topK[k]

    user_word_tag_tab = jieba.get_user_word_tag_tab()
    for wd,v in new_topK.iteritems():
        wscore = idf_freq.get(wd)
        find_wd = user_word_tag_tab.has_key(wd)
        #for solve the wrong cutting issue on the english. so i skip the english words output
        if (wscore is None or find_wd is True) and not re.match("^([a-zA-Z]+|\d+)$", wd):
            wsd = wd.encode('utf-8')
            #save the result into the new words collect file
            ff.write(wsd + " 10 n" + "\n")
            if find_wd is False:
                #add this word to the current dictionary
                jieba.add_word(wsd,10)

    if topK:
        ff.close
        return new_topK.keys()
    else:
        return tags
