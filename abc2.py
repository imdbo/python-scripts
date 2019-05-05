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

firefox_options = Options()
firefox_options.add_argument("")
#path for the web driver
driver = webdriver.Firefox(executable_path='d:/carl/geckodriver.exe', options=firefox_options)
driver.set_window_size(1920, 1080)
driver.get('https://www.abc.es/hemeroteca/resultados-busqueda-avanzada/todo?tod=brexit&rfec=20150101;20190424&nres=20')

def ret_links(process_count, summery_process, p):
    i = process_count - summery_process

    def get_and_find_words(link,l, i):
        url = link
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find("span", {"class": "titular"})
        article = soup.find("span", {"class": "cuerpo-texto"})
        article_text = article.findAll('p')
        print(title)
        print(article)
        print(article_text)
        with open('corpus-ABC.txt', 'a+') as c:
            c.write("[[" + str(l) + "--" + str(i) + "]]")
            c.write("\n")
            if title is not None:
                c.write(title.text)
            c.write("\n")
            for p in article_text:
                    if len(p.text) != 0 and p.text not in c:
                        c.write(p.text)
            c.write("\n")
            c.write("link: "+str(url))
            c.write("\n")
            time.sleep(0.5)

    while i < process_count:
        link_list = []
        driver.get("https://www.abc.es/hemeroteca/resultados-busqueda-avanzada/todo/pagina-" + str(i) + "?tod=brexit&rfec=20150101;20190424&nres=20")
        links = driver.find_elements_by_class_name("titulo")
        for a in range(len(links)):
            link = links[a].get_attribute('href')
            if  link is not None and len(link)> 0:
                link_list.append(link)
        for l in range(len(link_list)):
            try:
                get_and_find_words(link_list[l], l, i)
            except:
                continue
        i +=1
    driver.close()
    
if __name__ == '__main__':
    summery = driver.find_element_by_id("summery")
    summery = summery.text.split()
    summery = summery.pop()
    summery_total = int(summery)
    summery_process = math.floor(summery_total/5)
    process_count = summery_process
    driver.close()
    while(process_count < summery_total+1):
        p = 1
        parallel_retrieval = Process(target = ret_links, args=(process_count, summery_process, p))
        parallel_retrieval.start()
        process_count = process_count + summery_process
        p +=1
        time.sleep(2)