from django import template

register = template.Library()

# # 最多传两个参数
#
@register.filter  # multi_filer = register.filter(multi_filer)
def multi_filter(x,y):
    return x * y
#
#
# # 可以传任意多的参数
# @register.simple_tag()
# def multi_tag(x, y,z,v):
#     return x * y * z * v

# @register.filter(name="cut")
# def cut(value, arg):
#     return value.replace(arg, "")
#
# @register.filter(name='addstr')
# def add_str(arg,arg1):
#     return "{} {} mf !".formate(arg,arg1)

@register.filter(name='showSystemType')
def show_system_type(choice):
    system_type = {
        0: 'Linux',
        1: 'Windows'
    }
    system_type = system_type.get(choice)
    return system_type