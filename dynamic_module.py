'''
Requirements
1) Selenium Python3 module
2) Explici Python3 module
3) Firefox installed
4) Geckodriver
'''


import bs4 as bs
from bs4 import BeautifulSoup
import time
import re
from explicit import waiter
from selenium import webdriver

def getproductlink(main_url,url,tag,tag_class,sub_tag,sub_tag_class,llc):
    try:
        #Intialization of Webdriver and Provide Url. Opens new firefox windows. Warning: Do not close that window
        driver = webdriver.Firefox(executable_path='./geckodriver') 
        driver.get(url)
        
        #Dynamic Web page source
        page_src = driver.page_source

        #This part of code is to navigate page from top to button of screen
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            page_src_new = driver.page_source
            if(page_src != page_src_new):
                page_src = page_src_new
            else:    
                break

        #This part of code is to click the button/div/span after the lazy load        
        page_src = page_src_new 
        while True:
            #llc-(Lazy Load Class) Provide Css_selector. For ex. <div class="auto showmore"><button/span/div></div> give Css_selector as div.auto.showmore
            button = waiter.find_element(driver,llc)
            try:
                button.click()
                time.sleep(5)
            except:
                print("End of Loading")
            page_src_new = driver.page_source
            if(page_src != page_src_new):
                page_src = page_src_new
            else:
                break

        #finally provide the src code to beautiful soup
        soup = BeautifulSoup(page_src_new,'lxml')
        
        #program automatically closes the firefox window
        driver.close()
    except:
        print("Could access source page")
        driver.close()
        
    #This part of code is for find the tag in webpage 
    link=[]
    tag_l=[]
    try:
        tag_l = soup.find_all(str(tag),{"class":str(tag_class)})
        st ="\n".join(map(str,tag_l))
        lin = BeautifulSoup(st,'lxml')
        if tag_l:
            link = lin.find_all(str(sub_tag),{"class":str(sub_tag_class)})
    except:
        print("Tag/link not found. Probable tag/class-mismatch error.")

    #This part of code is for find the sub_tag and link in webpage 
    try:
        l = []
        if link:
            for i in link:
                atag = i.find_all('a')
                if "http" in atag[0]['href']:
                    l.append(atag[0]['href'])
                if "http" not in atag[0]['href'] and atag[0]['href']:
                    l.append(main_url+atag[0]['href'])
        s=set(l)
    except:
        print("Cound not find the Sub_tag/link")

    #To print the links in console enable the below code snippet
    '''
    j=0
    if s:
        for i in s:
            print(str(j)+" : "+i)
            j += 1'''
    return s

#To run the code individually enable anyone of  below code-snippets
'''
# BigBasket

main="https://www.bigbasket.com"
url=str("https://www.bigbasket.com/cl/fruits-vegetables/?nc=nb")
tag=str("div")
tag_c=re.sub(' +', ' ',str("ng-isolate-scope"))
sub_tag_class=re.sub(' +', ' ',str("col-sm-12 col-xs-5 prod-view ng-scope"))
sub_tag=str("div")
lazy_load_class = "div.show-more"
result = getproductlink(main,url,tag,tag_c,sub_tag,sub_tag_class,lazy_load_class)'''

'''
#Myntra
main="https://www.myntra.com"
url=str("https://www.myntra.com/mirrors")
tag=str("div")
tag_c=re.sub(' +', ' ',str("row-base"))
sub_tag_class=re.sub(' +', ' ',str("product-base"))
sub_tag=str("li")
lazy_load_class = "div.results-showMoreContainer"
result = getproductlink(main,url,tag,tag_c,sub_tag,sub_tag_class,lazy_load_class)'''

'''
main="https://www.snapdeal.com"
url=str("https://www.snapdeal.com/products/appliances-sandwich-makers?sort=plrty#bcrumbLabelId:2401")
tag=str("section")
tag_c=re.sub(' +', ' ',str("js-section clearfix dp-widget  dp-fired"))
sub_tag_class=re.sub(' +', ' ',str("product-tuple-image"))
sub_tag=str("div")
lazy_load_class = "div.col-xs-24.see-more-wrapper"
result = getproductlink(main,url,tag,tag_c,sub_tag,sub_tag_class,lazy_load_class)'''
