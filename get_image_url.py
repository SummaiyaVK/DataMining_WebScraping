import requests
import cssutils
import requests
import bs4 as bs
from bs4 import BeautifulSoup
import time
import urllib.request
import json
import re
import random
import string
import boto3
from boto3 import client
import contextlib
from io import BytesIO
import urllib3
import sys
from explicit import waiter
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urllib3.disable_warnings()

# Uses the creds in ~/.aws/credentials
session = boto3.Session(
    aws_access_key_id='AKIAJXNJCOAIZ4UPHP4A',
    aws_secret_access_key='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',
    region_name='ap-southeast-1'
)
region_name = 'ap-southeast-1'
s3 = session.resource('s3')
s3Client = session.client('s3')
# conn=client('s3')
# s3 = boto3.resource('s3')
bucket_name_to_upload_image_to = 's.demo.buckets'
folder = 'data-mining/TestFolder_oct30/'


def flipkart_scrape(url, html_element_name, element_type, name, rsltn, op_width, op_height, pid):
    sku_images = []
    final_urls = []
    rename_images = []
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='./geckodriver.exe',options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    cat = soup.find_all(html_element_name, {element_type: name})
    driver.close()
    try:
        image_links = [each.get('style') for each in cat]
        imagelinks = []
        for url in image_links:
            url = url.replace('background-image:url(', '').replace(')', '')
            imagelinks.append(url)
            # url=url.replace('128/128',lis[0]+'/'+lis[1])
            # print(url)
        if rsltn == 1:
            count = 1
            for url in imagelinks:
                url = re.sub(r'/\d\d\d/\d\d\d/', '/' + str(op_width) + '/' + str(op_height) + '/', url)
                url.find("?")
                url = url[:url.find("?")]
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_en = str_sku +  '-gito-' + str(count)
                name = strgen + ".jpeg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 2:
            count = 1
            for url in imagelinks:
                url = re.sub(r'_SS\d\d_', '_SS' + str(op_width) + '_', url)
                url.find("?")
                url = url[:url.find("?")]
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                strgen = str_sku + '-gito-' + str(count)
                name = strgen + ".jpeg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 3:
            count = 1
            for url in imagelinks:
                url = re.sub(r'_SS\d\d_', '_SS' + str(op_height) + '_', url)
                url.find("?")
                url = url[:url.find("?")]
                str_sku = random.choice(string.ascii_uppercase)+ random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                strgen = str_sku +  '-gito-' + str(count)
                name = strgen + ".jpeg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 4:
            print("In 4:")
            count = 1
            for url in imagelinks:
                url.find("?")
                url = url[:url.find("?")]
                str_sku = random.choice(string.ascii_uppercase)+ random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                strgen = str_sku + '-gito-' + str(count)
                name = strgen + ".jpeg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
    except:
        print("ERROR in flipkart")
    i = 0
    image_path = []
    for url in final_urls:
        with contextlib.closing(requests.get(url, stream=True, verify=False)) as response:
            # Set up file stream from response content.
            fp = BytesIO(response.content)
            # Upload data to S3
            print("Uploading")
            s3Client.upload_fileobj(fp, bucket_name_to_upload_image_to, folder + rename_images[i],
                                    ExtraArgs={'ACL': 'public-read'})
            path = 'https://s3-' + region_name + '.amazonaws.com/' + bucket_name_to_upload_image_to + '/' + folder + \
                   rename_images[i]
            image_path.append(path)
            print("uploaded")
        i = i + 1

    return image_path, sku_images
    # print(image_path)
    ''''
    for object in bucket_name_to_upload_image_to.objects.all():
        print(object)'''
    # for key in conn.list_objects(Bucket=bucket_name_to_upload_image_to)['Contents']:
    #    print(key)

    # print((image_links))

def myntra_scrape(url, html_element_name, element_type, name, rsltn, op_width, op_height, pid):
    sku_images = []
    final_urls = []
    rename_images = []
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='./geckodriver.exe',options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    cat = soup.find_all(html_element_name, {element_type: name})
    driver.close()
    try:
        image_links = [each.get('style') for each in cat]
        imagelinks = []
        for url in image_links:
            url_ = url.replace('background-image: url(', '').replace(');', '')
            # print(url_)
            imagelinks.append(url_)
            # url=url.replace('128/128',lis[0]+'/'+lis[1])
            # print(url)
        if rsltn == 1:
            count = 1
            for url in imagelinks:
                url = re.sub(r',w_\d\d\d', ',w_' + str(op_width), url)
                url = re.sub(r'/h_\d\d\d', '/h_' + str(op_height), url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku + str(pid) + '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 2:
            count = 1
            for url in imagelinks:
                url = re.sub(r',w_\d\d\d', ',w_' + str(op_width), url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku + str(pid) + '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 3:
            count = 1
            for url in imagelinks:
                url = re.sub(r'/h_\d\d\d', '/h_' + str(op_height), url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku + str(pid) + '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 4:
            count = 1
            for url in imagelinks:
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku + str(pid) + '-gito-' + str(count)
                name = str_gen + ".jpeg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
    except:
        print("ERROR in myntra")
    i = 0
    image_path = []
    for url in final_urls:
        with contextlib.closing(requests.get(url, stream=True, verify=False)) as response:
            # Set up file stream from response content.
            fp = BytesIO(response.content)
            # Upload data to S3
            print("Uploading")
            s3Client.upload_fileobj(fp, bucket_name_to_upload_image_to, folder + rename_images[i],
                                    ExtraArgs={'ACL': 'public-read'})
            path = 'https://s3-' + region_name + '.amazonaws.com/' + bucket_name_to_upload_image_to + '/' + folder + \
                   rename_images[i]
            image_path.append(path)
            print("uploaded")
        i = i + 1

    return image_path, sku_images


def image_scrape(url, html_element_name, element_type, name, rsltn, op_width, op_height, pid):
    sku_images = []
    final_urls = []
    rename_images = []
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='./geckodriver.exe',options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    cat = soup.find_all(html_element_name, {element_type: name})
    driver.close()
    # print(cat[0])
    try:
        img =  [each.find_all('img') for each in cat]
        print(img)
        image_links = []
        for each2 in img:
            for each1 in each2:
                if each1.get('src'):
                    image_links.append(each1.get('src'))
                if each1.get('lazysrc'):
                    image_links.append(each1.get('lazysrc'))

        # print(image_links)
        if rsltn == 1:
            count = 1
            for url in image_links:
                url = re.sub(r'/\d\d\d/\d\d\d/', '/' + str(op_width) + '/' + str(op_height) + '/', url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku + '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 2:
            count = 1
            for url in image_links:
                url = re.sub(r'_SS\d\d_', '_SS' + str(op_width) + '_', url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku +  '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 3:
            count = 1
            for url in image_links:
                url = re.sub(r'_SS\d\d_', '_SS' + str(op_height) + '_', url)
                str_sku = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku +  '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
        elif rsltn == 4:
            count = 1
            for url in image_links:
                # url = url.replace('128/128', lis[0] + '/' + lis[1])

                str_sku = random.choice(string.ascii_uppercase)+ random.choice(string.ascii_uppercase) + str(pid)
                sku_images.append(str_sku)
                str_gen = str_sku +  '-gito-' + str(count)
                name = str_gen + ".jpg"
                count = count + 1
                # url = url.replace('128/128', lis[0] + '/' + lis[1])
                final_urls.append(url)
                rename_images.append(name)
                print(url)
    except:
        print("ERROR!!")
    i = 0
    image_path = []
    for url in final_urls:
        with contextlib.closing(requests.get(url, stream=True, verify=False)) as response:
            # Set up file stream from response content.
            fp = BytesIO(response.content)
            # Upload data to S3
            print("Uploading")
            s3Client.upload_fileobj(fp, bucket_name_to_upload_image_to, folder + rename_images[i],
                                    ExtraArgs={'ACL': 'public-read'})
            path = 'https://s3-' + region_name + '.amazonaws.com/' + bucket_name_to_upload_image_to + '/' + folder + \
                   rename_images[i]
            image_path.append(path)
            print("uploaded")
        i = i + 1
    return image_path, sku_images


'''
    for i in final_urls:
        with contextlib.closing(requests.get(url, stream=True, verify=False)) as response:
        # Set up file stream from response content.
            fp = BytesIO(response.content)
        # Upload data to S3
            print("Uploading")
            s3Client.upload_fileobj(fp, bucket_name_to_upload_image_to, 'data-mining/Amazon/'+ url.split('/')[-1],ExtraArgs={'ACL':'public-read'})
            print("uploaded")
        #print("added")'''
