from web import models
import getpass
import subprocess
import random,string
import datetime,time
from multiprocessing import Process
from django.contrib.auth import authenticate
from CrazyEye import settings

class InteractiveHandler(object):
    '''负责与用户在命令行端所有的交互'''
    def __init__(self,*args,**kwargs):
        if self.authenticate():
            self.interactive()

    def get_random(self):
        random_data = ''.join(random.sample(string.ascii_lowercase,15))
        return random_data
    def authenticate(self):
        '''用户认证'''
        retry_count = 0
        while retry_count < 3:
            username = input("Username:").strip()
            if len(username) == 0: continue
            password = getpass.getpass("Password:")
            user = authenticate(username=username,password=password)
            if user is not None:
                print("\033[32:1m welcome %s\033[0m".center(50,'-'), user)
                self.user = user
                return True
            else:
                print("user or password is not correct.")
                retry_count += 1
        else:
            print("too many attempts.")
            return False


    def interactive(self):
        '''用户SHELL'''

        while True:
            print('''
            0  主机组
            1  主机
            ''')
            try:
                choice = input("[%s]" %(self.user)).strip()
                if choice == '0':
                    self.display_groups()
                elif choice == '1':
                    self.display_hosts()
                elif choice == 'exit':
                    break
                else:
                    continue
            except KeyboardInterrupt as e:
                pass



    def display_groups(self):
        exit_flag = False
        while not exit_flag:
            try:
                group_obj_list = self.user.host_groups.select_related()
                for index, group_obj in enumerate(group_obj_list):
                    print("%s. \t%s[%s]" % (index,
                                            group_obj,
                                            group_obj.bind_hosts.select_related().count()))
                user_choice = input("[%s]>>>" % (self.user)).strip()
                if user_choice.isdigit():
                    user_choice = int(user_choice)
                    if 0 <= user_choice < self.user.host_groups.select_related().count():
                        while True:
                            host_obj_list = group_obj.bind_hosts.select_related()
                            for index, host_obj in enumerate(host_obj_list):
                                print("%s. \t%s" % (index, host_obj.host))
                            host_choice = input("[%s]>>>" % (self.user)).strip()

                            if host_choice.isdigit():
                                host_choice = int(host_choice)
                                if 0 <= host_choice < host_obj_list.count():
                                    self.ssh_client_connect(host_obj_list[host_choice])
                            elif host_choice == 'exit':
                                break
                            else:
                                continue
                elif user_choice == 'exit':
                    exit_flag = True
                else:
                    continue
            except KeyboardInterrupt as e:
                pass

    def display_hosts(self):
        exit_flag = False

        while not exit_flag:
            try:
                host_obj_list = self.user.bind_host.select_related()
                for index, host_obj in enumerate(host_obj_list):
                    print("%s. \t%s" % (index, host_obj))
                host_choice = input("[%s]>>>" % (self.user)).strip()
                if host_choice.isdigit():
                    host_choice = int(host_choice)
                    if 0 <= host_choice < host_obj_list.count():
                        self.ssh_client_connect(host_obj_list[host_choice])
                elif host_choice == 'exit':
                    exit_flag = True
                else:
                    continue
            except KeyboardInterrupt as e:
                pass
    def ssh_client_connect(self,host_obj):
        random_data = self.get_random()
        p1 = Process(target=self.save_audit_log, args=(random_data,host_obj,))
        p1.start()
        p2 = Process(target=self.analysis_audit_log,args=(random_data,host_obj,))
        p2.start()
        cmd = "sshpass -p%s /usr/local/openssh8/bin/ssh -o StrictHostKeyChecking=no %s@%s -p%s -Z %s" %(host_obj.remote_user.password,host_obj.remote_user.username,host_obj.host.ip_addr,host_obj.host.port,random_data)
        subprocess.run(cmd,shell=True)

    def get_pid(self,random_data):
        cmd = """ps -ef|grep %s|grep -Ev "sshpass|grep"|awk '{print $2}'""" % (random_data)
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        pid = result.stdout.read().replace('\n', '').replace('\r\n', '')
        return pid

    def save_audit_log(self,random_data,host_obj):
        count = 0
        while count < 180:
            pid = self.get_pid(random_data)
            if pid.isdigit():
                now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                audit_cmd = 'strace -p %s -o %s/ssh_%s_%s_%s_%s_%s -t' %(pid,settings.AUDIT_LOG_DIR,host_obj.host.ip_addr,host_obj.remote_user.username,now,self.user,random_data)
                subprocess.Popen(audit_cmd,shell=True)
                break
            count += 1
            time.sleep(1)


    def analysis_audit_log(self,random_data,host_obj):
        Flag1 = False   # False 表示服务没有启用， True 表示服务启动了
        Flag2 = True  # False 表示服务没有启用， True 表示服务启动了
        while not Flag1:
            pid = self.get_pid(random_data)
            if pid.isdigit():
                Flag = True
                break
            time.sleep(1)
        while Flag2:
            pid = self.get_pid(random_data)
            if not pid.isdigit():
                Flag2 = False
                break
            time.sleep(1)
        # audit_log =

    