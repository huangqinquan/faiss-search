# -*- coding: UTF-8 -*-

import pymongo
from urllib import quote_plus
import numpy as np
import faiss



user = "root"
password = "root"
host = "192.168.199.115:20001"
uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)

np.set_printoptions(precision=16)


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


results = collec.find()#.limit(10)
for result in results:
    data = results.next()
    vector = data["input_vector"]
    xb.append(map(lambda x: x.to_decimal(), vector))
    # xb.append(vector)
    ids.append(data["id"])
    indexNum+=1
    if indexNum % 1000 == 0:
        print(indexNum)

print(xb[5])
# xb = np.array(xb).astype('float32')
# ids = np.array(ids).astype('int')
# print(xb[5])
# xq = np.atleast_2d(xb[5])

# index = faiss.IndexHNSWFlat(d, 1024)
# index_id = faiss.IndexIDMap(index)
#
# index_id.verbose = True
# index#.add(xb)
# index_id.add_with_ids(xb, ids)
#
# tmpindex = './index'
# faiss.write_index(index_id, tmpindex)


# print(xq)
# D,I = index.search(xq, 5)
# print("================")
# print(D)
# print("================")
# print(I)

