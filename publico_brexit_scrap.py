import selenium
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import math
import re
from multiprocessing import Process

def load_search():
    while True:
        try:
            driver.execute_script("window.history.go(-1)")
            if driver.current_url != 'https://www.elperiodico.com/es/buscador?size=15&query='+ word + '&rt=ZetaNews&video=false&order=score':
                driver.get('https://www.elperiodico.com/es/buscador?size=15&query='+ word + '&rt=ZetaNews&video=false&order=score')
            break
        except:
            pass
            print("searching for articles with the word "+ word + 'in https://www.elperiodico.com/es/buscador?size=15&query='+ word + '&rt=ZetaNews&video=false&order=score')
    #hide element obscuring website
    while True: 
        try:   
            time.sleep(0.5)
            driver.find_element_by_class_name("qc-cmp-button").click()
            break
        except: 
            break

def load_articles():
    while True:
        try:
            articles = driver.find_elements_by_class_name("thumb")
            break
        except:
            print('no results found for ' + word + '. running the search again')
            pass
    return articles

def get_and_find_words(link,l,t):
    url = link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find("h1", {"class": "title"})
    article = soup.find("div", {"class": "ep-detail-body"})
    article_text = article.findAll('p')
    with open('corpus.txt', 'a+') as c:
        c.write("[[" + str(t) + "--" + str(l) + "]]")
        c.write(title.text+"\n")
        for p in article_text:
            try:
                    if len(p.text) != 0 and p.text not in c:
                        c.write(p.text)
                        c.write("source: "+str(url))
            except:
                pass
    time.sleep(1)

def link_read(links_p, t):
    for l in range(len(links_p)):
        print(links_p[l])
        get_and_find_words(links_p[l],l,t)
        time.sleep(0.5)

if __name__ == '__main__':
        
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    #path for the web driver
    driver = webdriver.Firefox(executable_path='d:/carl/geckodriver.exe', options=firefox_options)
    driver.set_window_size(1920, 1080)
    word = 'brexit'
    p_in_text = []
    load_search()
    load_more = 100
    while True:
            if load_more > 1:
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                    cargarmas = driver.find_element_by_class_name("cargarmas")
                    cargarmas.click()
                    cargarmas.click()
                    print('loading more articles')
                    load_more = load_more-1
                except: 
                    break
            else:
                break
                
    articles = load_articles()
    list_links = []
    for a in range(len(articles)):
        print(len(articles))
        print(a)
        print(articles[a])
        try:
            link = articles[a].find_element_by_css_selector('a').get_attribute('href')
            list_links.append(link)
            print(len(list_links))
        except:
            pass

    driver.quit()

    def tally_split(link_tally):
        links_p = []
        tally_ls = math.floor(len(list_links)/link_tally)
        for l in range(link_tally):
            links_p.append(list_links[:tally_ls])
            del list_links[0:tally_ls]
        return links_p

    link_tally = math.floor(len(list_links)/5)
    if link_tally < 1 and len(list_links) != 0:
        link_tally = 1
        links_p = tally_split(link_tally)
    elif link_tally > 1:
        links_p = tally_split(link_tally)
            
    for t in range(link_tally):
        t = Process(target = link_read, args=(links_p[t],t))
        t.start()
