# encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default="female",max_length=10)
    address = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=11, blank=True, null=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png",max_length=200,verbose_name="用户头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.all().filter(user=self.id,has_read=False).count()
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱",max_length=50)
    send_type = models.CharField(choices=(('register','注册'),('forget','忘记密码'),('sendEmailCode','修改邮箱')),default="register",max_length=20,verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图",max_length=200)
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name