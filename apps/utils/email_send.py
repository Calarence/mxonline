# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/17 11:27'
from random import Random

from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length =len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

def sendRegisterEmail(email,send_type="register"):
    emailRecord = EmailVerifyRecord()
    code = random_str(16)
    emailRecord.code = code
    emailRecord.send_type = type
    emailRecord.email = email
    emailRecord.save()
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "幕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)
    elif send_type == 'forget':
        email_title = "幕学在线网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1:8000/reset/{0}".format(code)

    sendStatus = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if sendStatus:
        pass
