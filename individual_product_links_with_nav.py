'''import bs4 as bs
from bs4 import BeautifulSoup
import requests'''

'''def getproductlink(page_main_url,page_url,tag_name,tag_class,subtag,subtag_class,nav_tag,nav_tag_class):
    url_ = []
    amazon_request = requests.get(page_url)
    soup = BeautifulSoup(amazon_request.text, 'lxml')
    for paragraph in soup.find_all(str(nav_tag), class_= str(nav_tag_class)):
        for a in paragraph("a"):
            href = a.get('href')
            if "http" not in href:
                u = str(page_main_url) + href
                url_.append(u)
            else:
                url_.append(u)
    result = []
    for links in url_:
        amazon_request = requests.get(page_url)
        soup = BeautifulSoup(amazon_request.text, 'lxml')
        tag = soup.find_all(str(tag_name),{"class":str(tag_class)})
        link = tag[0].find_all(str(subtag),{"class":str(subtag_class)})
        l=[]
        if link:
            for i in link:
                atag=i.find_all('a')
                if "http" in atag[0]['href']:
                    l.append(atag[0]['href'])
                if "http" not in atag[0]['href'] and atag[0]['href']:
                    l.append(page_main_url+atag[0]['href'])
        s=set(l)
        j=0
        if s:
            for i in s:
                j += 1
        result.extend(s)
    return result'''

'''def getproductlinks(main_url,page_url,tag,tag_class,sub_tag,sub_tag_class,nav_tag,nav_tag_class):
    url_links = []   # navigate page links
    url_= []         # product links
    count = 0


    def getproductlink(url):
        amazon_request = requests.get(url)
        soup = BeautifulSoup(amazon_request.text, 'lxml')
        tag_l = soup.find_all(str(tag),{"class":str(tag_class)})
        link = tag_l[0].find_all(str(sub_tag),{"class":str(sub_tag_class)})
        l = []
        if link:
            for i in link:
                atag = i.find_all('a')
                if "http" in atag[0]['href']:
                    l.append(atag[0]['href'])
                if "http" not in atag[0]['href'] and atag[0]['href']:
                    l.append(main_url+atag[0]['href'])
        s=set(l)
        j=0
        if s:
            for i in s:
                #print(str(j)+" : "+i)
                j += 1
        return s



    def initialize_recipe(page_url):
        url_str = str(page_url)
        req = requests.get(url_str)
        s = BeautifulSoup(req.text, 'lxml')
        return s


    def navigate_page(soup):
        for paragraph in soup.find_all(str(nav_tag), class_=str(nav_tag_class)):
            for a in paragraph("a"):
                href = a.get("href")
                if "http" not in href:
                    u = str(main_url) + href
                    #print(u)
                    url_links.append(u)
                else:
                    #print("in loop")
                    u = href
                    #print(u)
                    url_links.append(u)

                if type == "recursive":
                    if len(url_links) <= 5:
                        sp_ = initialize_recipe(u)
                        navigate_page(sp_)


    url_s = str(page_url)
    r = requests.get(url_s)
    s = BeautifulSoup(r.text, 'lxml')
    for paragraph in s.find_all(str(nav_tag), class_=str(nav_tag_class)):
        for a in paragraph("a"):
            count = count + 1
    if (count > 1):
        type = "normal"
    else:
        type = "recursive"

    print(type)
    sp = initialize_recipe(page_url)
    navigate_page(sp)
    for i in url_links:
        print(i)

    for links in url_links:
        url_l = str(links)
        s=getproductlink(url_l)
        url_.extend(s)
    for i in url_:
        print(i)
    return url_'''

import bs4 as bs
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def getproductlinks(main_url,page_url,tag,tag_class,sub_tag,sub_tag_class,nav_tag,nav_tag_class):
    url_links = []   # navigate page links
    url_= []         # product links
    count = 0


    def getproductlink(url):
        try:
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Firefox(executable_path='./geckodriver.exe',options=options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            time.sleep(2)
            driver.close()
        except Exception as error:
            print("Could access source page")
            print(error)
        try:
            tag_l = soup.find_all(str(tag),{"class":str(tag_class)})
            st ="\n".join(map(str,tag_l))
            lin = BeautifulSoup(st,'lxml')
            if tag_l:
                link = lin.find_all(str(sub_tag),{"class":str(sub_tag_class)})
        except:
            print("Tag/link not found. Probable tag/class-mismatch error.")
        try:
            l = []
            if link:
                for i in link:
                    atag = i.find_all('a')
                    if "http" in atag[0]['href']:
                        l.append(atag[0]['href'])
                    if "http" not in atag[0]['href'] and atag[0]['href']:
                        l.append(main_url+atag[0]['href'])
        except:
            print("Cound not find the Sub_tag/link")
        s=set(l)
        j=0
        if s:
            for i in s:
                #print(str(j)+" : "+i)
                j += 1
        return s




    def initialize_recipe(page_url):
        url_str = str(page_url)
        req = requests.get(url_str)
        s = BeautifulSoup(req.text, 'lxml')
        return s


    def navigate_page(soup):
        for paragraph in soup.find_all(str(nav_tag), class_=str(nav_tag_class)):
            for a in paragraph("a"):
                href = a.get("href")
                if "http" not in href:
                    u = str(main_url) + href
                    #print(u)
                    url_links.append(u)
                else:
                    #print("in loop")
                    u = href
                    #print(u)
                    url_links.append(u)

                if type == "recursive":
                    if len(url_links) <= 5:
                        sp_ = initialize_recipe(u)
                        navigate_page(sp_)


    url_s = str(page_url)
    r = requests.get(url_s)
    s = BeautifulSoup(r.text, 'lxml')
    for paragraph in s.find_all(str(nav_tag), class_=str(nav_tag_class)):
        for a in paragraph("a"):
            count = count + 1
    if (count > 1):
        type = "normal"
    else:
        type = "recursive"

    print(type)
    sp = initialize_recipe(page_url)
    navigate_page(sp)
    url_links = list(set(url_links))
    for i in url_links:
        print(i)

    for links in url_links:
        url_l = str(links)
        s=getproductlink(url_l)
        url_.extend(s)
    for i in url_:
        print(i)
    return url_
