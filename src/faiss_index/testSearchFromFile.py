# -*- coding: UTF-8 -*-

import numpy as np
import faiss

index_file = "pipeline_c579da36fa77d1be7cc53bb9d7044038"

file = open(index_file)

d = 128
xb = []
ids = []

num = 0

lines = file.readlines(10)


for line in lines:
    arr = line.strip().replace(' ', '').split(',', 1)
    id = arr[0]

    if id == 'id':
        continue

    try:
        ids.append(int(id))
    except:
        print("==========error id = " + id)
        continue

    vector = np.array(arr[1].strip('[]').split(',')).astype('float32')
    xb.append(vector)
    num += 1

xb = np.array(xb)
ids = np.array(ids)

print(ids)
print("读取到内存完毕")
print("==========================")
index_file_path = "./test/ivf100_" + index_file + ".index"
index = faiss.read_index(index_file_path)

index.nprobe = 10
# index.hnsw.efSearch = 256
scores, neighbors = index.search(xb, 10)

print(neighbors)