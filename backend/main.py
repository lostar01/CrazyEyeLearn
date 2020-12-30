from backend import interactive

class ManagementUtily(object):
    def __init__(self,sys_args):
        self.sys_args = sys_args
        self.argv_verify()

    def argv_verify(self):
        if len(self.sys_args) < 2:
            self.show_help_msg()
        else:
            if hasattr(self,self.sys_args[1]):
                func = getattr(self,self.sys_args[1])
                func(self.sys_args)
            else:
                self.show_help_msg()

    def show_help_msg(self):
        msg = '''
        run     启动堡垒机用户终端
        '''
        print(msg)

    def run(self,*args,**kwargs):
        '''启动用户交互程序'''
        interactive.InteractiveHandler(*args,**kwargs)

