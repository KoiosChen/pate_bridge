from app import default_api, logger
from flask_restplus import Resource, reqparse, fields
from app.decorate import permission_ip
from app.docker import jobs
from app.common import success_return, false_return

return_dict = {'code': fields.String(required=True, description='success | false'),
               'data': fields.Raw(description='string or json'),
               'message': fields.String(description='成功或者失败的文字信息')}

pate_bridge_ns = default_api.namespace('algocap', path='/algocap',
                                       description='抓包脚本配置下载接口')

return_json = pate_bridge_ns.model('ReturnRegister', return_dict)

PermissionIP = ['10.100.25.238', '127.0.0.1']

job_parser = reqparse.RequestParser()
job_parser.add_argument('image', required=True, help='image名称')
job_parser.add_argument('futures_contract', help='合约名称')
job_parser.add_argument('product_name', help='产品名称')


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
        image_name = args['image']
        product_name = args['product_name']
        contract_name = args['futures_contract']
        try:
            return success_return(data=jobs.start(image_name, product_name, contract_name))
        except Exception as e:
            logger.error(str(e))
            return false_return(), 404
