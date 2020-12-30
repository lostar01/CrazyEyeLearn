from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
class IDC(models.Model):
    '''机房'''
    name = models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

class Host(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField()
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey('IDC',blank=True,null=True,on_delete=models.CASCADE)
    system_type_choices = ((0,'linux'),(1,'Windows'))
    system_type = models.SmallIntegerField(choices=system_type_choices,default=0)
    memo = models.CharField(max_length=128,blank=True,null=True)
    enable = models.BooleanField(default=1,verbose_name='启用本机')

    class Meta:
        unique_together = ('ip_addr','port')

    def __str__(self):
        return "%s(%s)" %(self.hostname,self.ip_addr)

class RemoteUser(models.Model):
    '''存储远程用户信息'''
    auth_type_choices = ((0,'ssh-password'),(1,'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    username = models.CharField(max_length=128)
    aliasname = models.CharField(max_length=128,default="")
    password = models.CharField(max_length=256,help_text="如果auth_type选择为ssh-key,那么此处应该为key 的路径")

    class Meta:
        unique_together = ('auth_type','username','password')

    def __str__(self):
        return "%s(%s)" %(self.username,self.aliasname)



class BindHost(models.Model):
    '''关联远程主机与远程用户'''
    host = models.ForeignKey('Host',on_delete=models.CASCADE)
    remote_user = models.ForeignKey('RemoteUser',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('host','remote_user')

    def __str__(self):
        return "<%s:%s>" %(self.host.hostname,self.remote_user.username)

# class UserProfile(models.Model):
#     '''堡垒机用户'''
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.name


class HostGroups(models.Model):
    '''主机组'''
    name = models.CharField(max_length=64,unique=True)
    bind_hosts = models.ManyToManyField('BindHost',blank=True)
    memo = models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name

class SessionRecord(models.Model):
    '''记录SSH 会话'''
    user = models.ForeignKey('UserProfile',verbose_name='堡垒机账号',on_delete=models.CASCADE)
    bind_host = models.ForeignKey('BindHost',on_delete=models.CASCADE)
    rand_tag = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s  %s>" %(self.user.email,self.bind_host)

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    bind_host = models.ManyToManyField('BindHost',blank=True)
    host_groups = models.ManyToManyField('HostGroups',blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class AuditLog(models.Model):
    token = models.CharField(max_length=256,unique=True)
    status_type_choice = ((0,"websocket not connect"),(1,"websocket open"),(2,"websocket close"))
    status = models.SmallIntegerField(choices=status_type_choice,default=0)
    audit_log = models.CharField(max_length=256,blank=True)

    def __str__(self):
        return self.audit_log

class CmdRecord(models.Model):
    ops_time = models.DateTimeField()
    ops_user = models.EmailField(
        verbose_name='ops user',
        max_length=255
    )
    host = models.GenericIPAddressField()
    host_user = models.CharField(max_length=128)
    cmd = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.cmd
