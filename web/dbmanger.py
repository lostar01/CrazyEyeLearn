from web.models import AuditLog,CmdRecord

def create_auditlog_obj(token):
    AuditLog.objects.create(token=token)

def get_auditlog_obj(token):
    audit_obj = AuditLog.objects.filter(token=token)
    return audit_obj

def update_auditlog_obj(audit_obj,**kwargs):
    rs = audit_obj.update(**kwargs)
    return rs
def get_auditlog_objs(status):
    audit_objs = AuditLog.objects.filter(status=status)
    return audit_objs

#create CmdRecord obj
def create_cmdrecord_obj(ops_user,host,host_user,cmd_list):
    obj_list = []
    for cmd in cmd_list:
        obj = CmdRecord()
        obj.ops_user = ops_user
        obj.host = host
        obj.host_user = host_user
        obj.ops_time = cmd[0]
        obj.cmd = cmd[1]
        obj_list.append(obj)

    result = CmdRecord.objects.bulk_create(obj_list)
    return result


