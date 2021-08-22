from app import default_api, logger, work_q
from flask_restplus import Resource, reqparse, fields
from app.decorate import permission_ip
from app.docker import jobs
from app.type_validation import check_semicolon
from app.common import success_return, false_return
import uuid
import traceback
import re

return_dict = {'code': fields.String(required=True, description='success | false'),
               'data': fields.Raw(description='string or json'),
               'message': fields.String(description='成功或者失败的文字信息')}

pate_bridge_ns = default_api.namespace('启动策略', path='/pate',
                                       description='通过POST方法启动指定合约的策略')

return_json = pate_bridge_ns.model('ReturnRegister', return_dict)

PermissionIP = ['10.100.25.238', '127.0.0.1', '192.168.16.121']

job_parser = reqparse.RequestParser()
job_parser.add_argument('image', required=True, type=check_semicolon, help='image名称')
job_parser.add_argument('network', required=True, type=check_semicolon, help='网络映射配置，格式：ip:service_port:source_port')
job_parser.add_argument('futures_contract', type=check_semicolon, help='合约名称')
job_parser.add_argument('product_name', type=check_semicolon, help='产品名称')


@pate_bridge_ns.route('/start_contract')
class PateBridge(Resource):
    @pate_bridge_ns.doc(body=job_parser)
    @pate_bridge_ns.marshal_with(return_json)
    @permission_ip(PermissionIP)
    def post(self, **kwargs):
        """
        启动指定合约
        """
        args = job_parser.parse_args()
        job_id = str(uuid.uuid4())
        docker_run = {"job_id": job_id,
                      "network_mapping": args['network'],
                      "image_name": args['image'],
                      "product_name": args['product_name'],
                      "futures_contract": args['futures_contract']}
        try:
            work_q.put(docker_run)
            return success_return(data={"id": job_id}, message="job is put in the queue.")
        except Exception as e:
            logger.error(str(e))
            traceback.print_exc()
            return false_return(), 404
