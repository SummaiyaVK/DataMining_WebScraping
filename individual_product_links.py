import bs4 as bs
from bs4 import BeautifulSoup
import requests

def getproductlink(page_main_url,page_url,tag_name,tag_class,subtag,subtag_class):
    amazon_request = requests.get(page_url)
    soup = BeautifulSoup(amazon_request.text, 'lxml')
    tag = soup.find_all(str(tag_name),{"class":str(tag_class)})
    #print(tag)
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
            #print(str(j)+" : "+i)
            j += 1
    return s

#Testing
"""
getproductlink("https://www.amazon.in","https://www.amazon.in/digital-slr-cameras/b/ref=sd_allcat_sbc_tvelec_dslr?ie=UTF8&node=1389177031","div","a-row s-result-list-parent-container","div","s-item-container")
print('amazon-over')
getproductlink("https://www.flipkart.com","https://www.flipkart.com/mobiles/pr?sid=tyy%2F4io&p%5B%5D=facets.brand%255B%255D%3DApple&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&otracker=clp_metro_expandable_1_1.metroExpandable.METRO_EXPANDABLE_iPhone_apple-products-store_44444444444444444444444444444444444444444490ff40fd-a46b-4a40-9440-fbe783136afb_DesktopSite&fm=neo%2Fmerchandising&iid=M_7a8d634c-bd86-4742-b4c4-f0a5966b4bc1_1.90ff40fd-a46b-4a40-9440-fbe783136afb_DesktopSite&ppt=Homepage&ppn=Homepage&ssid=9o20v86neo0000001536758749808","div","_1HmYoV _35HD7C col-10-12","div","_1UoZlX")
"""
