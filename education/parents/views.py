#-*- encoding=utf-8 -*-

'''
Created on 2019年6月6日

@author: yaachou
'''

from cart.cart import Cart
from django.shortcuts import render, redirect
from agency.models import Lessons
from django.http import HttpResponse, HttpResponseNotFound

from parents.processing.processing import *

email_temp = ''
validation = ''

# Create your views here.
def index(request):      
    return render(request, 'index.html')


# 注册账号
def register(request):
    return render(request, 'register.html')


def register_check(request):

    # 判断是否为已登录状态
    if request.session.get('username'):
        return HttpResponse('抱歉，您已登录，请先注销登录当前账户！')
    else:
        pass

    register_type = request.GET['register_type']
    email = request.GET['email']
    
    # 全局变量，便于调用
    global validation, email_temp
    email_temp = email

    # 若为已绑定邮箱则发送邮件并记录验证码
    result = vali_email(email)
    # result = '1234'

    if result != '':
        validation = result
    else:
        return HttpResponse('抱歉，邮件发送失败！请返回输入正确邮箱或检查网络连接！')

    html = '../../register_' + register_type + '.html'
    return redirect(html)


def register_parent(request):
    return render(request, 'register_parent.html')


def register_teacher(request):
    return render(request, 'register_teacher.html')

def register_agency(request):
    return render(request, 'register_agency.html')


# 注册信息审核
def get_regi_info(request):
    
    # 获取注册表单信息
    username = request.POST['username']
    password = request.POST['password']
    validation_got = request.POST.get('code')
    name = request.POST['name']
    phone = request.POST['phone']
    child_name = request.POST['child_name']
    child_age = request.POST['child_age']
    child_sex = request.POST['child_sex']

    global email_temp
    email = email_temp
    
    # 初始化错误提醒error_warning
    error_warning = ''
    
    # 若无错误则注册，否则弹出错误信息
    if username_check(username)!=True:
        error_warning = username_check(username)
    elif password_check(password)!=True:
        error_warning = password_check(password)
    elif phone_check(phone)!=True:
        error_warning = phone_check(phone)
    else:
        print(validation_got, validation)
        if validation_got == validation:
            
            User.objects.create(username=username, password=password)
            Parents.objects.create(username=username, email = email, phone = phone, name = name,  \
                                    child_name = child_name, child_age = child_age, child_sex = child_sex)
            '''
            user = Parents()
            user.username = username
            user.email = email
            user.phone = phone
            user.name = name
            user.child_name = child_name
            user.child_age = child_age
            user.child_sex = child_sex
            user.save()
            '''
        else:
            error_warning = '抱歉，验证码错误或已失效，请重新获取！'   
    if len(error_warning) == 0:
        return HttpResponse('注册成功！')
    else:
        return HttpResponse(error_warning)

# 获取邮箱并发送验证码
def get_validation(request):
    
    # 判断是否为已登录状态
    if request.session.get('username'):
        return HttpResponse('抱歉，您已登录，请先注销登录当前账户！')
    else:
        pass
    
    # 获取用户输入的邮箱
    email = request.GET['email']
    
    # 全局变量，便于调用
    global validation
    
    # 若为未绑定邮箱则提示
    try:
        user = Parents.objects.get(email = email)
    except Parents.DoesNotExist:
        return render(request, 'retrive.html', {'error': '抱歉，无此用户！'})    

    # 若为已绑定邮箱则发送邮件并记录验证码
    result = vali_email(email)
    if result:
        validation = result
        return render(request, 'password_reset.html', {'user': user})
    else:
        return render(request, 'get_validation.html')


# 获取用户输入的验证码及新密码
def password_reset(request):
    
    # 判断是否为已登录状态
    if request.session.get('username'):
        return HttpResponse('抱歉，您已登录，请先注销登录当前账户！')
    else:
        pass
    
    # 获取实际验证码用户输入的信息
    username = request.POST['username']
    got_validation = request.POST['validation']
    new_password = request.POST['new_password']
    reconfirm = request.POST['reconfirm']
    
    # 输入出错则提示
    if got_validation != validation:
        return render(request, 'password_reset.html')
    elif new_password != reconfirm:
        return render(request, 'password_reset.html')
    
    # 输入正确则更新数据库
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return render(request, 'password_reset.html')
    finally:
        user.password = new_password
        user.save()
    return True


# 登录界面
def login(request):
    return render(request, 'login.html')


# 登录时检查（账号、密码正确则跳转主界面；否则输出错误信息！）
def login_check(request):
    
    # 获取登录表单信息
    username = request.POST['username']
    password = request.POST['password']
    
    # 若无错误则登录，否则弹出错误信息
    try:
        u = User.objects.get(username = username)           
        if u.password == password:            
            # 已经登录，弹出“重复登录”提示信息
            if request.session.get('username'):
                return HttpResponse('您已登录，不要重复登录！')           
            # 未登录，则建立session并跳转到主界面
            else:
                request.session['username'] = username
                return render(request, 'index.html')       
        # 密码错误
        else:
            return HttpResponse('对不起，密码输入错误！')      
    except (UnboundLocalError, User.DoesNotExist):
        # 用户不存在
        return HttpResponse('抱歉，该用户不存在！')
        

# 登录状态下展示用户信息
def display_info(request):
    username = request.session.get('username')
    if request.method == 'POST':
        return HttpResponseNotFound('<h1>Page not found</h1>')
    elif username:
        user1 = User.objects.get(username = username)
        user2 = Parents.objects.get(username = username)
        
        # 构建信息列表方便传到html
        # info_list = {'username':username, 'email':user1.email, 'mobile':user1.mobile, 'name':user2.name, 'balance':user2.balance ,user2.child_name, user2.child_age, user2.child_sex}
        return render(request, 'parents/show_info.html', {'user1': user1, 'user2': user2})
    else:
        return HttpResponse('请先登录！')


# 修改用户信息
def alter_info(request):
    
    # 获取用户信息表单内容
    email = request.POST['email']
    phone = request.POST['phone']
    name = request.POST['name']
    child_name = request.POST['child_name']
    child_age = request.POST['child_age']
    child_sex = request.POST['child_sex']

    if '@' not in email:
        return HttpResponse('邮箱格式错误，请检查！')
    
    if len(phone) != 11:
        return HttpResponse('手机格式错误，请检查！')


    # 获取当前登录用户
    username = request.session.get('username')

    user1 = User.objects.get(username = username)
    user2 = Parents.objects.get(username = username)
    try:
        user1.email = email
        user1.mobile = phone
        user2.name = name
        user2.child_name = child_name
        user2.child_age = child_age
        user2.child_sex = child_sex
        user1.save()
        user2.save()
    except:
        return HttpResponse('抱歉,保存失败,请检查重试！')    
    return redirect('../display_info/')


# 根据关键字查询课程信息
def seek_lessons(request):
    
    # 判断是否为已登录状态
    if request.session.get('username'):
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 获取关键字和带有关键字的课程信息（若为空，则显示全部课程信息）
    keywords = request.GET['keywords']
    show_list = Lessons.objects.filter(cname__icontains=keywords)
    
    return render(request, 'parents/display_info.html', {'show_list': show_list})


# 申请试听
def apply_listening(request):
    
    # 判断是否为已登录状态
    username = request.session.get('username')
    if username:
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 判断为申请试听（保存信息）还是取消试听（删除信息）并提示
    apply_listening = request.GET['apply_listening']
    if apply_listening:
        user = Parents.objects.get(username = username)
        user_name = user.name
        phone = user.phone
        return HttpResponse('已成功申请！')
    else:
        return HttpResponse('已取消申请！')


# 对试听效果做出评价
def comment(request):
    
    # 获取当前登录用户的用户名
    username = request.session.get('username')
    
    # 判断是否为已登录状态
    if username:
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 获取表单评价内容及课程名
    stars = request.GET['stars']
    words = request.GET['words']
    lesson_id = request.GET['lesson_id']
    
    # 将评价存入数据库
    comment_item = Comments.objects.get(username = username, lesson_id = lesson_id)

    comment_item.stars = stars
    comment_item.words = words
    comment_item.save()
    
    return


# 展示课程信息
def display_lessons(request):
    return render(request, 'lessons_list.html')


# 添加到购物车（默认数量为一）
def add_to_cart(request):
    
    # 判断是否为已登录状态
    username = request.session.get('username')
    if username:
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 添加到购物车
    lesson_id = request.GET['lesson_id']
    lesson = Lessons.objects.get(lesson_id=lesson_id)
    cart = Cart(request)
    cart.add(lesson, lesson.cprice, 1)
    return redirect('../get_cart/')


# 根据课程id从购物车移除
def remove_from_cart(request):
    lesson_id = int(request.GET['lesson_id'])
    lesson = Lessons.objects.get(lesson_id=lesson_id)
    cart = Cart(request)
    cart.remove(lesson)
    return redirect('../get_cart/')


# 获取购物车内容
def get_cart(request):
    
    # 判断是否为已登录状态
    username = request.session.get('username','')
    if username:
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 返回购物车内容
    return render(request, 'parents/cart.html', {'cart': Cart(request)})


# 付款购买课程
def pay(request):
    
    # 判断是否为已登录状态
    username = request.session.get('username')
    if request.session.get('username'):
        pass
    else:
        return HttpResponse('抱歉，您还未登录，请先登录！')
    
    # 获取登录用户余额信息及待付款
    user = Parents.objects.get(username = username)
    balance = user.balance
    cost = request.GET.get('cost')
    
    # 判断余额是否充足
    if balance > int(float(cost)):
        balance -= sum
        return HttpResponse('付款成功！')
    else:
        return HttpResponse('抱歉，余额不足！\n请联系管理员进行充值（qq:123456789）')
    

# 注销登录
def logout(request):
    try:
        del request.session['username']
    except:
        return HttpResponse('抱歉，您还未登录！')
    finally:
        return HttpResponse('注销登录成功！')
