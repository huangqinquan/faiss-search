# -*- coding: UTF-8 -*-

from flask import Flask
from faiss_index import blueprint as FaissIndexBlueprint
import logging

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(FaissIndexBlueprint.blueprint)


if __name__ == '__main__':
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    app.run(threaded=True, debug=True, use_reloader=False)


