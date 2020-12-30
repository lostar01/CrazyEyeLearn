from web.models import AuditLog

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