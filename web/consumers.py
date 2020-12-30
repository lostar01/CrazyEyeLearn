from channels.generic.websocket import WebsocketConsumer
from django.http import QueryDict
import json,os,io,datetime
from backend.ssh import SSH
from CrazyEye.settings import AUDIT_LOG_DIR
from backend.utils import get_loger
from web.models import BindHost
from web import dbmanger

class SshConsumer(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def connect(self):
        """
        打开 websocket 连接, 通过前端传入的参数尝试连接 ssh 主机
        :return:
        """
        self.accept()
        query_string = self.scope.get('query_string')
        ssh_args = QueryDict(query_string=query_string, encoding='utf-8')
        print("ssh_args===",ssh_args)

        width = ssh_args.get('width')
        height = ssh_args.get('height')


        width = int(width)
        height = int(height)
        bhid = ssh_args.get('bhid')
        djuser = ssh_args.get('djuser')
        token = ssh_args.get('token')
        host=None
        port = None
        user = None
        passwd = None
        auth = None

        if bhid:
            try:
                bind_host_obj = BindHost.objects.get(pk=bhid)
                port = bind_host_obj.host.port
                host = bind_host_obj.host.ip_addr
                user = bind_host_obj.remote_user.username
                passwd = bind_host_obj.remote_user.password
                auth = bind_host_obj.remote_user.auth_type

            except:
                print("bindhost id is not exist.")
                self.close()

        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        audit_file_name = 'ssh_%s_%s_%s_%s.log' %(host,user,now,djuser)

        self.audit_obj = dbmanger.get_auditlog_obj(token=token)

        if self.audit_obj:
            self.loger = get_loger(AUDIT_LOG_DIR,audit_file_name)
            self.ssh = SSH(websocker=self, message=self.message)
            dbmanger.update_auditlog_obj(self.audit_obj,status=1,audit_log=os.path.join(AUDIT_LOG_DIR,audit_file_name))
        else:
            self.close()

        ssh_connect_dict = {
            'host': host,
            'user': user,
            'port': port,
            'timeout': 30,
            'pty_width': width,
            'pty_height': height,
            'password': passwd
        }
        if auth == 1:
            ssh_key_file = passwd
            with open(ssh_key_file, 'r') as f:
                ssh_key = f.read()

            string_io = io.StringIO()
            string_io.write(ssh_key)
            string_io.flush()
            string_io.seek(0)
            ssh_connect_dict['ssh_key'] = string_io

            os.remove(ssh_key_file)

        self.ssh.connect(**ssh_connect_dict)

    def disconnect(self, close_code):
        try:
            dbmanger.update_auditlog_obj(self.audit_obj, status=2)
            self.ssh.close()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        self.loger.info(data)
        if type(data) == dict:
            status = data['status']
            if status == 0:
                data = data['data']
                self.ssh.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.ssh.resize_pty(cols=cols, rows=rows)
