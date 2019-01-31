# -*- coding: UTF-8 -*-

import pymongo
from urllib import quote_plus
import numpy as np
import faiss
import bson.decimal128



user = "root"
password = "root"
host = "192.168.199.115:20001"
uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)

np.set_printoptions(precision=16)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold=np.inf)

#向量维度
d=300
xb = []
ids = []
#一页翻5000条
pageNum = 200

connection=pymongo.MongoClient(uri,20001)
db=connection.get_database("mongo_test") #.alpsfiles
collec = db.get_collection("pipeline_c579da36fa77d1be7cc53bb9d7044038")

count = 200
#游标
indexNum = 0


results = collec.find().limit(10)
for result in results:
    data = results.next()
    vector = data["input_vector"]
    xb.append(map(lambda x: x.to_decimal(), vector))
    ids.append(data["id"])
    indexNum+=1
    if indexNum % 1000 == 0:
        print(indexNum)

xb = np.array(xb).astype('float32')

print str(xb[0]).replace('n', '')
print ids[0]

# ids = np.array(ids).astype('int')
# print(ids)
#
# index_file_path = "./index"
# index = faiss.read_index(index_file_path)
#
# scores, neighbors = index.search(xb, 20)
#
# print(neighbors)