import selenium
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import re

firefox_options = Options()
firefox_options.add_argument("--headless")
#path for the web driver
driver = webdriver.Firefox(executable_path='c:/SCRAP/geckodriver.exe', options=firefox_options)
driver.set_window_size(1920, 1080)
word = 'brexit'
p_in_text = []

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

def get_and_find_words(l):
    url = l
    print(l)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find("h1", {"class": "title"})
    article = soup.find("div", {"class": "ep-detail-body"})
    article_text = article.findAll('p')
    print(title.text)
    for p in article_text:
        print(p.text)
        with open('corpus.txt', 'a+', encoding="utf-8") as c:
            print('writing text')
            if len(p.text) != 0 and p.text not in c:
                c.write(p.text)
            else:
                pass

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
scraped_links =  0
for l in (list_links):
    #avoid race condition marionette ?
    driver.get(l)
    get_and_find_words(l)
    scraped_links = scraped_links+1
    time.sleep(0.5)

driver.quit()

#regex cleanup /// 
pattern = r"([\/]){1}[\s]+[\w]+([áéíóúÁÉÍÓÚ])?(([^\v][\w]+)?([^\v][\w]+)+([\s][\(][\w]+[\)])?)?"
with open('test.txt', 'r+', encoding="utf-8") as c:
    text =  c.read()
    final_text = re.sub(pattern, '', text)
    with open('final_text.txt', 'w+', encoding="utf-8") as f:
        f.write(final_text)