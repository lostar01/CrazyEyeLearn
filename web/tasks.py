from __future__ import absolute_import

from celery import shared_task
from web import dbmanger
from backend.wsaudit import AuditLogHandler


#from celery.task import tasks
#from celery.task import Task

@shared_task(bind=True)
def analy_audit(self):
    audit_obj = dbmanger.get_auditlog_objs(2)
    rs_list = []
    for obj in audit_obj:
        log_file = obj.audit_log
        parm_list = log_file.split('_')
        host = parm_list[2]
        host_user = parm_list[3]
        ops_user = parm_list[5].split('.log')[0]
        parser = AuditLogHandler(log_file)
        cmd_list = parser.parse()
        print(host,host_user,ops_user,cmd_list)
        rs = dbmanger.create_cmdrecord_obj(ops_user,host,host_user,cmd_list)
        rs_list.append(rs)
        # change the auditlog status
        obj.status = 3
        obj.save()
    return len(rs_list)
