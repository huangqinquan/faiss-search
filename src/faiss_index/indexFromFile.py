# -*- coding: UTF-8 -*-

import numpy as np
import faiss

index_file = "pipeline_e4648947f89f5e18207b2f70950a199a"

f_xb = "e_xb.bin.17312364"
f_ids = "e_ids.bin.17312364"

d=128

xb = np.fromfile(f_xb, dtype='float32')
ids = np.fromfile(f_ids, dtype='int')
xb.shape = len(ids), d

# index = faiss.index_factory(d, "PCA32,IMI2x12,Flat")
index = faiss.index_factory(d,"PCA32,IVF100,PQ8 ")
# index = faiss.index_factory(d, "IVF100，PQ8")
# index = faiss.IndexHNSWFlat(d, 32)
# index.hnsw.efConstruction = 40
index.verbose = True

index_id = faiss.IndexIDMap(index)


index.train(xb)
print("train complete")
index_id.add_with_ids(xb, ids)
print("add complete")


tmpindex = './ivf100_' + index_file + '.index'
faiss.write_index(index_id, tmpindex)
print("write compelte")
