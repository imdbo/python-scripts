import math
import codecs
import re
from nltk.corpus import stopwords
from multiprocessing import Process
from nltk.tokenize import word_tokenize
from nltk.corpus import gutenberg

stopwords = set(stopwords.words("german"))
english = set([w.lower() for w in gutenberg.words()])
def word_process(text_words):
    english_list = []
    print("hello")
    for w in text_words:
        if w.lower() in english and w.lower() not in stopwords and len(w) > 1:
            english_list.append(w)
            with open("sido_english.txt", "a+", encoding="utf-8") as se:
                se.write(w+",")
    print(english_list)

def create_ps(ps):
    tally_ps = math.floor(len(text_words)/ps)
    for p in range(ps):
        w_p_p.append(text_words[0:tally_ps])
        del text_words[0:tally_ps+1]
        print(len(w_p_p[p]))
        
if __name__ == '__main__':
    source = input("type full path of the file you want to read. Stopwords will be excluded: ")
    w_p_p = []
    with codecs.open (source, "r+", encoding="utf8") as tw:
        tw = tw.read()
        text_words = re.findall(r"\w+", tw)
        ps = math.floor(len(text_words)/3000)
        if ps < 1 and len(text_words) != 0:
            ps = 1
            create_ps(ps)
        elif ps >= 1:
            create_ps(ps)
        for p in range(ps):
            p = Process(target = word_process, args= (w_p_p[p],))
            p.start()
