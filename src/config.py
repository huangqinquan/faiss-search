# -*- coding: UTF-8 -*-

import numpy as np
import ConfigParser
from urllib import quote_plus

DEBUG = True

def getconfig(filename,section=''):
    cf=ConfigParser.ConfigParser()   #实例化
    cf.read(filename)   #读取配置文件
    cf_items = dict(cf.items(section)) if cf.has_section(section)  else {}  #判断SECTION是否存在,存在把数据存入字典,没有返回空字典
    return cf_items

def REBUILD_INDEX():

    conf=getconfig('faiss.conf','mongo')

    print "rebuild index!!!!!!!!!!!!!!!!!!!!!!"
    #先模拟几个步骤

    user = conf["user"]
    password = conf["pwd"]
    host = conf["host"]
    port = conf["port"]
    database = conf["database"]

    # #当独立一个库的时候就可以遍历所有collection
    # collection = "pipeline_c579da36fa77d1be7cc53bb9d7044038"
    #
    # #向量维度
    # d=300
    # xb = []
    #
    # uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)
    # connection=pymongo.MongoClient(uri,port)
    # db=connection.get_database(database)
    # collec = db.get_collection(collection)
    # results = collec.find()
    # for result in results:
    #     xb.append(result["input_vector"])


    # return "rebuild index"

def GET_FAISS_INDEX():
    import os
    import faiss

    index_dict = {}


    base_path = os.path.abspath(os.path.join(os.path.abspath('.'), "..")) + '/resource/index_file/'
    models = os.listdir(base_path)
    for model in models:
        file_path = model + '/'
        file_name = 'index'
        index_file_path = base_path + file_path + file_name
        index = faiss.read_index(index_file_path)
        index_dict[model] = index
    return index_dict


UPDATE_FAISS_AFTER_SECONDS = None
