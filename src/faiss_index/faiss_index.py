import faiss
import numpy as np
import time
from flask import current_app

class FaissIndex(object):

    def __init__(self, index_dict):
        assert index_dict

        self.index_dict = index_dict

    # def search_by_ids(self, ids, k):
    #     vectors = [self.id_to_vector(id_) for id_ in ids]
    #     results = self.__search__(ids, vectors, k + 1)
    #
    #     return results

    def search_by_vectors(self, vectors, k, model):
        ids = [None] * len(vectors)
        results = self.__search__(ids, vectors, k, model)

        return results

    def __search__(self, ids, vectors, k, model):
        def neighbor_dict(id_, score):
            return { 'id': long(id_), 'score': float(score) }

        def result_dict(id_, vector, neighbors):
            return { 'id': id_, 'vector': vector.tolist(), 'neighbors': neighbors }

        # results = []
        t0 = time.time()
        out_dict = {}
        out_dict['output_vector']=[]
        out_dict['code']=1

        vectors = [np.array(vectors, dtype=np.float32)]
        vectors = np.atleast_2d(vectors)

        index = self.index_dict[model]

        faiss.omp_set_num_threads(1)


        scores, neighbors = index.search(vectors, k) if vectors.size > 0 else ([], [])



        for id_, vector, neighbors, scores in zip(ids, vectors, neighbors, scores):
            # neighbors_scores = zip(neighbors, scores)
            # neighbors_scores = [(n, s) for n, s in neighbors_scores if n != id_ and n != -1]
            # neighbors_scores = [neighbor_dict(n, s) for n, s in neighbors_scores]
            # out_dict = result_dict(id_, vector, neighbors_scores)

            out_dict['output_vector'] = neighbors.tolist()
            out_dict['code'] = 0


        t1 = time.time()

        current_app.logger.info("faiss use : %7.4f second",  (t1 - t0))

        return out_dict
