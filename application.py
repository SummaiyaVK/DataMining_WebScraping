from flask import Flask, render_template, request, flash
import csv
import json
import individual_product_links_with_nav as indi_links
import get_product_details as get_pd
import get_image_url as get_img
from pymongo import MongoClient
import boto3
import MySQLdb
import dynamic_module
from datetime import datetime

app = Flask(__name__,template_folder='./')
app.secret_key = 'some_secret'

global count
count=0
global links_len
links_len=0

@app.route('/')
def home():
    return render_template('side_bar_page.html')

@app.route('/create_recipe_page.html')
def create_recipe():
    return render_template('create_recipe_page.html')

@app.route('/result_create',methods=['post'])
def create():
    recipe_name=request.form['recipename']
    main_url=request.form['page_main_url']
    url=request.form['page_url']
    tag=request.form['main_tag']
    tag_class=request.form['main_class_name']
    sub_tag = request.form['sub_tag']
    sub_tag_class = request.form['sub_class_name']
    title_tag=request.form['title_tag']
    title_class=request.form['title_class']
    pd_tag=request.form['pd_tag']
    pd_class=request.form['pd_class']
    img_ele=request.form['img_ele']
    img_ele_type=request.form['img_ele_type']
    img_ele_name=request.form['img_ele_name']
    ps_tag=request.form['ps_tag']
    ps_class=request.form['ps_class']
    ps_format=request.form['ps_format']
    ps_label_class=request.form['ps_label_class']
    ps_form_class=request.form['ps_form_class']
    nav_tag=request.form['nav_tag']
    nav_tag_class=request.form['nav_tag_class']
    op_height=request.form['op_height']
    op_width=request.form['op_width']
    category=request.form['category']
    sub_category=request.form['sub_category']
    dynamic_class=request.form['dynamic_class']


    connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'sa123')
    cursor = connection.cursor()
    connection.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')    # get the cursor
    cursor.execute("USE gito") # select the database

    last_recipe_id_query = 'select max(id) from recipe;'
    cursor.execute(last_recipe_id_query)
    connection.commit()
    for ans in cursor.fetchall():
        var=ans
    if var[0]!=None:
        recipe_insert_query='insert into recipe(id,recipe_name,main_url,url,tag,tag_class,sub_tag,sub_tag_class,title_tag,title_class,pd_tag,pd_class,img_ele,img_ele_type,img_ele_name,ps_tag,ps_class,ps_format,ps_label_class,ps_form_class,nav_tag,nav_tag_class,op_height,op_width,category,sub_category,dynamic_class) values(' +str(var[0]+1)+","+ "'"+recipe_name+"'" +','+"'"+main_url +"'"+ ','+"'" + url +"'"+ ','+"'"+ tag +"'"+ ',' +"'"+ tag_class+"'"+','+"'"+ sub_tag+"'" + ',' +"'"+sub_tag_class +"'"+ ',' +"'"+ title_tag+"'"+','+"'"+title_class+"'"+","+ "'"+pd_tag+"'"+","+"'"+pd_class+"'"+","+"'"+img_ele+"'"+","+"'"+img_ele_type+"'"+","+"'"+img_ele_name+"'"+","+"'"+ps_tag+"'"+","+"'"+ps_class+"'"+","+"'"+ps_format+"'"+","+"'"+ps_label_class+"'"+","+"'"+ps_form_class+"'"+","+"'"+nav_tag+"'"+","+"'"+nav_tag_class+"'"+","+"'"+op_height+"'"+","+"'"+op_width+"'"+","+"'"+category+"'"+","+"'"+sub_category+ "'"+","+"'"+dynamic_class+"'"+");"
        cursor.execute(recipe_insert_query)
        connection.commit()
    else:
        recipe_insert_query='insert into recipe(id,recipe_name,main_url,url,tag,tag_class,sub_tag,sub_tag_class,title_tag,title_class,pd_tag,pd_class,img_ele,img_ele_type,img_ele_name,ps_tag,ps_class,ps_format,ps_label_class,ps_form_class,nav_tag,nav_tag_class,op_height,op_width,category,sub_category,dynamic_class) values(' +str(1)+","+ "'"+recipe_name+"'" +','+"'"+main_url +"'"+ ','+"'" + url +"'"+ ','+"'"+ tag +"'"+ ',' +"'"+ tag_class+"'"+','+"'"+ sub_tag+"'" + ',' +"'"+sub_tag_class +"'"+ ',' +"'"+ title_tag+"'"+','+"'"+title_class+"'"+","+ "'"+pd_tag+"'"+","+"'"+pd_class+"'"+","+"'"+img_ele+"'"+","+"'"+img_ele_type+"'"+","+"'"+img_ele_name+"'"+","+"'"+ps_tag+"'"+","+"'"+ps_class+"'"+","+"'"+ps_format+"'"+","+"'"+ps_label_class+"'"+","+"'"+ps_form_class+"'"+","+"'"+nav_tag+"'"+","+"'"+nav_tag_class+"'"+","+"'"+op_height+"'"+","+"'"+op_width+"'"+","+"'"+category+"'"+","+"'"+sub_category+ "'"+","+"'"+dynamic_class+"'"+");"
        cursor.execute(recipe_insert_query)
        connection.commit()

    return render_template('create_recipe_page_1.html')

@app.route('/execute_recipe_page',methods=['get'])
def execute_recipe_page():
    connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'sa123')
    cursor = connection.cursor()
    connection.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')    # get the cursor
    cursor.execute("USE gito") # select the database
    return_value_fetch=[]
    execute_recipe_fetch_query = 'select * from recipe;'
    cursor.execute(execute_recipe_fetch_query)
    connection.commit()
    for fetch_i in cursor.fetchall():
        return_value_fetch.append(fetch_i)
    flash('Started scraping')
    return render_template('execute_recipe_page.html',return_value_fetch=return_value_fetch)



@app.route('/result_execute',methods=['post'])
def result():
    img_path_string = ""
    sku_img_string = ""
    connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'sa123')
    cursor = connection.cursor()
    connection.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')    # get the cursor
    cursor.execute("USE gito") # select the database

    '''outfile = open('Details.csv','w+', newline='')
    writer = csv.writer(outfile)
    writer.writerow(["Title", "Product_description","Specs"])'''
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')


    option=request.form['selected']

    cursor.execute('select * from recipe where id = (%s)',(option))
    connection.commit()

    for recipe_fields in cursor.fetchall():
        #print('extracting feilds from db')
        recipe_name=recipe_fields[1]
        main_url=recipe_fields[2]
        url=recipe_fields[3]
        tag=recipe_fields[4]
        tag_class=recipe_fields[5]
        sub_tag = recipe_fields[6]
        sub_tag_class = recipe_fields[7]
        title_tag=recipe_fields[8]
        title_class=recipe_fields[9]
        pd_tag=recipe_fields[10]
        pd_class=recipe_fields[11]
        img_ele=recipe_fields[12]
        img_ele_type=recipe_fields[13]
        img_ele_name=recipe_fields[14]
        ps_tag=recipe_fields[15]
        ps_class=recipe_fields[16]
        ps_format=recipe_fields[17]
        ps_label_class=recipe_fields[18]
        ps_form_class=recipe_fields[19]
        nav_tag=recipe_fields[20]
        nav_tag_class=recipe_fields[21]
        op_height=recipe_fields[22]
        op_width=recipe_fields[23]
        category=recipe_fields[24]
        sub_category=recipe_fields[25]
        dynamic_class=recipe_fields[26]

    type=0
    if op_height=='' and op_width=='':
        type=4
    elif op_height=='':
        type=2
    elif op_width=='':
        type=3
    else:
        type=1

    #img_paths=[]
    global count
    global links_len

    if dynamic_class=='':
        print(dynamic_class+'hello')
        links=indi_links.getproductlinks(main_url,url,tag,tag_class,sub_tag,sub_tag_class,nav_tag,nav_tag_class)
    else:
        print(dynamic_class+'hello inside else')
        links=dynamic_module.getproductlinks(main_url,url,tag,tag_class,sub_tag,sub_tag_class,dynamic_class)
    print(links)
    links_len=len(links)
    for link in links:
        img_paths=[]
        db_storage_dict={}
        count=count+1
        req_list=get_pd.extract_title_des(link,title_tag,title_class,pd_tag,pd_class)
        if ps_label_class=='':
            ps_label_class=None
        if ps_form_class=='':
            ps_form_class=None
        prod_specs=get_pd.product_details(link,ps_tag,ps_class,ps_format,ps_label_class,ps_form_class)
        last_product_id_query = 'select max(id) from product;'
        cursor.execute(last_product_id_query)
        connection.commit()
        for ans in cursor.fetchall():
            var=ans
        print('Passing this value {0}'.format(var[0]))
        try:
            if "flipkart.com" in link:
                if var[0]!=None:
                    img_paths,sku_images=get_img.flipkart_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,int(var[0])+1)
                    print(img_paths)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]
                else:
                    print("Inside else")
                    img_paths,sku_images=get_img.flipkart_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,1)
                    print(img_paths)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]
            elif "myntra.com" in link:
                if var[0]!=None:
                    img_paths,sku_images=get_img.myntra_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,int(var[0])+1)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]
                else:
                    img_paths,sku_images=get_img.myntra_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,1)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]
            else:
                if var[0]!=None:
                    img_paths,sku_images=get_img.image_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,int(var[0])+1)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]
                else:
                    img_paths,sku_images=get_img.image_scrape(link, img_ele, img_ele_type, img_ele_name,type,op_width,op_height,1)
                    img_path_string=""
                    for path in img_paths[0:len(img_paths)-1]:
                        img_path_string+=path+'|'
                    img_path_string+=img_paths[-1]
                    sku_img_string=""
                    for path in sku_images[0:len(sku_images)-1]:
                        sku_img_string+=path+'|'
                    sku_img_string+=sku_images[-1]

            print(img_paths)
        except Exception as er:
            print(er)
        if len(req_list)==1:
            req_list.append('NA')
        req_list.append(json.dumps(prod_specs))

        '''img_path_string=""
        for path in img_paths[0:len(img_paths)-1]:
            img_path_string+=path+'|'
        img_path_string+=img_paths[-1]

        sku_img_string=""
        for path in sku_images[0:len(sku_images)-1]:
            sku_img_string+=path+'|'
        sku_img_string+=sku_images[-1]'''
        try:
            if var[0]!=None:
                sql_product_query =  'insert into product(id,source,product_name,product_overview,category,sub_category,image_path,sku,created_at) values(' +str(var[0]+1)+","+ "'"+main_url+"'" +','+"'"+req_list[0] +"'"+ ','+"'" + req_list[1] +"'"+ ','+"'"+ category +"'"+ ',' +"'"+ sub_category +"'"+','+"'"+ img_path_string+"'" + ',' +"'"+ sku_img_string +"'"+ ',' +"'"+ formatted_date+"');"
            else:
                sql_product_query =  'insert into product(id,source,product_name,product_overview,category,sub_category,image_path,sku,created_at) values(' +'1,'+ "'"+main_url+"'" +','+"'"+req_list[0] +"'"+ ','+"'" + req_list[1] +"'"+ ','+"'"+ category +"'"+ ',' +"'"+ sub_category +"'"+','+"'"+ img_path_string+"'" + ',' +"'"+ sku_img_string +"'"+ ',' +"'"+ formatted_date+"');"
            cursor.execute(sql_product_query)
            connection.commit()
            for key in prod_specs:
                #print(key)
                #print(prod_specs[key])
                last_spec_id_query = 'select max(id) from specification;'
                cursor.execute(last_spec_id_query)
                connection.commit()
                for ans1 in cursor.fetchall():
                    var1=ans1
                if var[0]!=None:
                    if var1[0]!=None:
                        sql_spec_query = 'insert into specification(id,product_id,specification_name,specification_value,created_at) values('+str(var1[0]+1)+',' +str(var[0]+1)+','+"'"+key+"'"+','+"'"+str(prod_specs[key])+"'"+','+"'"+ formatted_date+"');"
                    else:
                        sql_spec_query = 'insert into specification(id,product_id,specification_name,specification_value,created_at) values('+str(1)+',' +str(var[0]+1)+','+"'"+key+"'"+','+"'"+str(prod_specs[key])+"'"+','+"'"+ formatted_date+"');"
                else:
                    if var1[0]!=None:
                        sql_spec_query = 'insert into specification(id,product_id,specification_name,specification_value,created_at) values('+str(var1[0]+1)+',' +str(1)+','+"'"+key+"'"+','+"'"+str(prod_specs[key])+"'"+','+"'"+ formatted_date+"');"
                    else:
                        sql_spec_query = 'insert into specification(id,product_id,specification_name,specification_value,created_at) values('+str(1)+',' +str(1)+','+"'"+key+"'"+','+"'"+str(prod_specs[key])+"'"+','+"'"+ formatted_date+"');"
                #print(sql_spec_query)
                cursor.execute(sql_spec_query.encode('utf-8'))
                connection.commit()
        except:
            pass
    return "<h3>Written to tables</h3>"

@app.route('/progress',methods=['get'])
def details():
    global links_len
    global count
    return render_template('progress.html',links_len=links_len,count=count)

app.run(debug=True)
