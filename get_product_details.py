import sys
import requests
import bs4 as bs
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen,Request
import json
import re

def extract_title_des(page_url,title_tag,title_class,des_tag,des_class):
    l = []
    amazon_request = requests.get(page_url)
    soup = BeautifulSoup(amazon_request.text, 'lxml')
    title = soup.find_all(str(title_tag),{"class":str(title_class)})
    des = soup.find_all(str(des_tag),{"class":str(des_class)})
    if title:
        if title[0].find('p'):
            l.append(title[0].find('p').text.strip())
        else:
            l.append(title[0].text.strip())
    if des:
        if des[0].find('p'):
            l.append(des[0].find('p').text.strip())
        else:
            l.append(des[0].text.strip())
    print(l)
    return l

'''def product_details(link,element_type,class_name,given_format,label_class,value_class):
    #note on given_format
    #1-multi-table
    #2-ul-li
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    techD=soup.find_all(element_type,{'class':class_name})
    #print(techD)
    product_specs={}
    spec_table = techD[0].find_all('table')
    if given_format=="1":
        for i in range(len(spec_table)):
            for spec_row in spec_table[i].find_all('tr'):
                #print(spec_row)
                #print(' ')
                if label_class==None and value_class==None:
                    spec_and_value=spec_row.find('td')
                    print(spec_and_value)
                else:
                    spec=spec_row.find('td',{'class':label_class})
                    value=spec_row.find('td',{'class':value_class})
                    #print(spec,value)
                if spec!=None and value!=None:
                    product_specs[spec.text]=value.text
    #print(product_specs)
    return product_specs'''

'''def product_details(link,element_type,class_name,given_format,label_class,value_class):
    #note on given_format
    #1-multi-table
    #2-ul-li
    product_specs={}
    try:
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        techD=soup.find_all(element_type,{'class':class_name})
        product_specs={}
        spec_table = techD[0].find_all('table')
        print(len(spec_table))
        if given_format=="1":
            for i in range(len(spec_table)):
                for spec_row in spec_table[i].find_all('tr'):
                    if label_class==None and value_class==None:
                        spec_and_value=spec_row.find('td')
                        if spec_and_value!=None:
                            req_list=spec_and_value.text.strip().split('\n')
                            if len(req_list)!=1:
                                dict_key=req_list[0]
                                dict_value={}
                                i=1
                                while i+1<len(req_list):
                                    if req_list[i]=='':
                                        i+=1
                                    else:
                                        dict_value[req_list[i]]=req_list[i+1]
                                        i+=2
                                product_specs[dict_key]=dict_value
                    else:
                        spec=None
                        value=None
                        spec=spec_row.find('td',{'class':label_class})
                        value=spec_row.find('td',{'class':value_class})
                        #print(spec,value)
                        if spec!=None and value!=None:
                            product_specs[spec.text]=value.text
    except Exception as err:
        print(err)
    print(product_specs)
    return product_specs'''

def product_details(link,element_type,class_name,given_format,label_class,value_class):
    #note on given_format
    #1-multi-table
    #2-ul-li
    try:
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        techD=soup.find_all(element_type,{'class':class_name})
        product_specs={}
        spec_table = techD[0].find_all('table')
        print(len(spec_table))
        if given_format=="1":
            for i in range(len(spec_table)):
                for spec_row in spec_table[i].find_all('tr'):
                    if label_class==None and value_class==None:
                        spec_and_value=spec_row.find('td')
                        if spec_and_value!=None:
                            req_list=spec_and_value.text.strip().split('\n')
                            if len(req_list)!=1:
                                dict_key=req_list[0]
                                dict_value={}
                                i=1
                                while i+1<len(req_list):
                                    if req_list[i]=='':
                                        i+=1
                                    else:
                                        dict_value[req_list[i]]=req_list[i+1]
                                        i+=2
                                product_specs[dict_key]=dict_value
                        product_specs1={}
                        for key in product_specs:
                            if type(product_specs[key])==type({'key':'value'}):
                                for key2 in product_specs[key]:
                                    product_specs1[key2]=product_specs[key][key2]
                            else:
                                product_specs1[key]=product_specs[key]
                        product_specs=product_specs1
                    else:
                        spec=None
                        value=None
                        spec=spec_row.find('td',{'class':label_class})
                        value=spec_row.find('td',{'class':value_class})
                        #print(spec,value)
                        if spec!=None and value!=None:
                            product_specs[spec.text]=value.text
    except:
        print("Max conn exception.. Waiting to Reconnect")
        time.sleep(10)
    #print(product_specs)
    return product_specs
