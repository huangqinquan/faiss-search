# -*- coding: UTF-8 -*-


import numpy as np
import faiss
import gc

index_file = "pipeline_e4648947f89f5e18207b2f70950a199a"

file = open(index_file)

d = 128
xb = []
ids = []

num = 0
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
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

        # if num % 1000000 == 0:
        #     xb = np.array(xb)
        #     ids = np.array(ids)
        #     xb.tofile("c_xb.bin." + str(num))
        #     ids.tofile("c_ids.bin." + str(num))
        #     xb = []
        #     ids = []
        #     gc.collect()

    print(num)



    # print(num)

print("读取到内存完毕")


xb = np.array(xb)
ids = np.array(ids)

xb.tofile("e_xb.bin." + str(num))
ids.tofile("e_ids.bin." + str(num))

# index = faiss.index_factory(d, "PCA32,IMI2x12,PQ8")
# index = faiss.index_factory(d,"PCA32,IVF100,PQ8 ")
# index.verbose = True
# index.train(xb)
#
# index.add_with_ids(xb[0:50, :], ids[0:50])
# index.add_with_ids(xb[51:100, :], ids[51:100])
#
# tmpindex = './' + index_file + '.index'
# faiss.write_index(index, tmpindex)
