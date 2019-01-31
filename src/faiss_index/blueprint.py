# -*- coding: UTF-8 -*-

from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import BadRequest
from faiss_index import FaissIndex
from multiprocessing.dummy import Pool as ThreadPool
import json
import time
import logging

try:
    import uwsgi
except ImportError:
    print('Failed to load python module uwsgi')
    print('Periodic faiss index updates isn\'t enabled')

    uwsgi = None

blueprint = Blueprint('faiss_index', __name__)

out_error_dict = {}
out_error_dict['output_vector']=[]
out_error_dict['code']=1



@blueprint.route('/ping')
def ping():
    return "pong"

# 程序启动后执行一次
@blueprint.record_once
def record(setup_state):
    print('=====start=====')
    manage_faiss_index(
        setup_state.app.config['GET_FAISS_INDEX'],
        setup_state.app.config['REBUILD_INDEX']
    )

@blueprint.route('/test', methods=['POST'])
def test():
    t0 = time.time()
    test = request.get_json(force=True)
    t1 = time.time()
    current_app.logger.info("test receive params use : %7.4f second",  (t1 - t0))
    return str(test)

@blueprint.route('/faiss/search', methods=['POST'])
def search():
    try:
        t0 = time.time()
        jsonstr = request.get_json(force=True)

        #验证json字符串合法性
        validate(jsonstr, {
            'type': 'object',
            'required': ['k'],
            'properties': {
                'k': { 'type': 'integer', 'minimum': 1 },
                'pipeline_index': { 'type': 'string'},
                'input_vector': {
                    'type': 'array',
                    'items': { 'type': 'number' }
                    # 'items': {
                    #     'type': 'array',
                    #     'items': { 'type': 'number' }
                    # }
                },
                'query': { 'type': 'string'}
            }
        })
        #开始搜索向量
        t1 = time.time()
        current_app.logger.info("check use : %7.4f second",  (t1 - t0))
        results_vectors = blueprint.faiss_index.search_by_vectors(jsonstr['input_vector'], jsonstr['k'], jsonstr['pipeline_index']) if 'input_vector' in jsonstr else []
        t2 = time.time()
        current_app.logger.info("search use : %7.4f second",  (t2 - t0))

        # return jsonify(results_vectors)
        return json.dumps(results_vectors)

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        # return 'Bad request', 400
        return json.dumps(out_error_dict)

    except Exception as e:
        print('Server error', e)
        # return 'Server error', 500
        return json.dumps(out_error_dict)

#指定index的名字，然后去mongo库中生成到本地
def add_index(index_name):
    collection = "pipeline_" + index_name

# 读取索引等基本工作
def manage_faiss_index( get_faiss_index, rebuild_index ):

    SIG_REBUILD_INDEX = 1

    def rebuild_periodically(signal = None):
        rebuild_index()

    #定时重建索引
    def set_periodically():
        print("定时")
        uwsgi.register_signal(SIG_REBUILD_INDEX, 'workers', rebuild_periodically)
        # uwsgi.add_timer(SIG_REBUILD_INDEX, 5)
        #每周周一晚上一点重建索引
        uwsgi.add_cron(SIG_REBUILD_INDEX, 0, 1, -1, -1, 1)

    def set_faiss_index():
        print('Getting Faiss index')
        blueprint.faiss_index = FaissIndex(get_faiss_index())

    if uwsgi:
        set_periodically()

    set_faiss_index()