import nltk
import re
import math
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process
#from selenium.webdriver.support.ui import Select

        
def word_tally(split_text):
    words_dict = {}
    word_list = []
    #max number of words per process. 50k
    counted_words = 0
    #split text into 10k words blocks
    for i in range(len(split_text)):
        counted_words = counted_words+1
        print('word n '+ str(i) +'counted '+ str(counted_words))
        if i+1 not in range(len(split_text)):
            print("it's bigger!")
            counted_words = 0
            word_list.append(split_text[i])
            words_dict["list "+ str(i)] = word_list
            word_list = []
        elif counted_words < 50000:
            word_list.append(split_text[i])
            print(split_text[i])
        elif counted_words == 50000:
            counted_words = 0
            words_dict["list "+ str(i)] = word_list
            word_list = []
    for k in words_dict:
        k = Process(target = run_drive, args=(words_dict[k],))
        k.start()

def run_drive(split_corpus):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path='d:\carl\geckodriver.exe', options=firefox_options)

    def get_and_find_words(w):
        #cambridge works fine... maybe
        driver.get('https://dictionary.cambridge.org/dictionary/english/'+w)
        print('looking for the word ' + w)
        counter = 2
        entry = 0
        while counter > 0:
            try:    
                entry = driver.find_element_by_class_name('headword')
                counter = counter -1
            except:
                break
        if entry != 0 and w in entry.text:
            print(w + ' FOUND')
            #final text with words found in an english dictionary
            with open('sido_english.txt', 'a+', encoding='utf-8') as fc:
                fc.write(w + ",")
        else:
            print(w+ ' not found')

    for w in split_corpus:
        w = w.lower()
        if 'ß' not in w:
            get_and_find_words(w)
        else:
            pass

    driver.close()

def tally_scan(m_tally):
    tally_ws = math.floor(len(split_text)/m_tally)
    print(tally_ws)
    for m in range(m_tally):
            tally_dict["tally_"+ str(m)] = split_text[0:tally_ws]
            del split_text[0:tally_ws+1]
            print(len(tally_dict["tally_"+str(m)]))

if __name__ == '__main__':
    #full corpus with german & english
    x = open("d:\carl\sido_full.txt", encoding="utf-8")
    text = x.read()
    split_text = re.findall(r'\w+', text)
    #split the initial word tally into different processes. 50k words each.
    m_tally = math.floor(len(split_text)/50000)
    print(m_tally)
    tally_dict = {}
    if m_tally < 1 and  len(split_text) != 0:
        m_tally = 1
        tally_scan(m_tally)
    elif m_tally >= 1:
        tally_scan(m_tally)
    for t in tally_dict:
        t = Process(target = word_tally, args=(tally_dict[t],))
        t.start()
    x.close()
