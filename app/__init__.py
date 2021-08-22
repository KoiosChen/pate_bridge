from flask import Flask, request
import logging
import queue
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

# class SQLAlchemy(SQLAlchemyBase):
#     def apply_driver_hacks(self, app, info, options):
#         super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
#         options['poolclass'] = NullPool
#         options.pop('pool_size', None)


# 用于存放监控记录信息，例如UPS前序状态，需要配置持久化

default_api = Api(title='AlgoSpace Dispatch API', version='v0.1', prefix='/api', contact='jinzhang.chen@algospace.com')

# 用于处理订单建议书的队列
work_q = queue.Queue(maxsize=100)

# 用于处理请求request的队列
request_q = queue.Queue(maxsize=1000)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()
hdlr = logging.FileHandler("pate_bridge.log")
formatter = logging.Formatter(fmt='%(asctime)s - %(module)s-%(funcName)s - %(levelname)s - %(message)s',
                              datefmt='%Y/%m/%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


def create_app(config_name):
    app = Flask(__name__)
    default_api.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    from .job import job as jobs_blueprint
    app.register_blueprint(jobs_blueprint)

    return app
