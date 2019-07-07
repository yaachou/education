#-*- encoding=utf-8 -*-

'''
Created on 2019年6月6日

@author: yaachou
'''

from django.core.mail import send_mail
from parents.models import *
import random


# ͨ通过<yaachou@qq.com>向指定邮箱<to_mail>发送主题为<subject>、内容为<mail_content>的邮件
def mail(to_email, subject, email_content):
    # 发送方邮箱
    from_email = 'yaachou@qq.com'
    # to_email = '1768887421@qq.com'
    # email_content = '亲爱的小伙伴，你好~\n你的验证码为:1234'
    try:
        send_mail(subject, email_content, from_email, [to_email], fail_silently=False)
    except:        
        # 发送失败
        return 0
    return 1


# 检查用户名（ 未被注册且为字母及下划线组合，长度为3-15位）
def username_check(username):
    if len(username)<3 or len(username)>15:
        return '用户名长度错误！'
    else:
        try:
            Users.objects.get(username = username)
        except Users.DoesNotExist:
            print('1')
            for i in username:
                if i<'A' or (i>'Z' and i<'a') or i>'z' and i!='_':
                    return '用户名出现非法字符！'
                else:
                    pass
            return True
        print(username)
        return '抱歉，该用户已存在，换个试试？'


# 检查密码
def password_check(password):
    if len(password)<6 or len(password)>15:
        return '密码过长或过短！'
    return True


# 生成验证码并发送
def vali_email(email):
    to_email = email
    subject = 'education-app注册（测试）'
    validation = ''
    for i in range(4):
        validation += str(random.randint(1,9))
    email_content = '小伙伴，你好~\n你的验证码为：' + validation
    if mail(to_email, subject, email_content) == 1:
        return validation
    else:
        return ''
    
    
# 检查手机号
def phone_check(phone):
    if len(phone)!=11:
        return '手机号出错！'
    else:
        return True