from django.shortcuts import render,HttpResponse,HttpResponseRedirect,render_to_response,redirect
from django.views.generic import View 
from django.views import generic
from django.shortcuts import get_object_or_404
from agency.forms import *
from agency.util import Util
from agency.models import *
from users.models import *
from users.forms import *
from helpers import get_page_list, AdminUserRequiredMixin, ajax_required, SuperUserRequiredMixin, send_html_email
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
#①教育机构用户登录后，可见店面选择、店面课程表、试听申请列表、
#信息修改、通知公告、个人信息六个选项。
#②个人教师用户登录后，可见课程表、试听申请列表、信息修改、通
#知公告、个人信息五个选项。
class AgencyIndex(View):
    '''首页'''
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        notice=Notice.objects.all().order_by('notice_time')[0:20]
        if username=='': ##未登录
            uf=UserForm()
            return redirect('home')
        else:
            return render(request,"agency/AgencyIndex.html",{'username':username,'notice':notice})     ##已登录

class TeacherIndex(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        notice=Notice.objects.all().order_by('notice_time')[0:20]
        if username=='': ##未登录
            return redirect('home')
        else:
            return render(request,"agency/TeacherIndex.html",{'username':username,'notice':notice})     ##已登录

'''    
class AgencyLogin(View):
    def get(self, request):
        uf=UserForm()
        return render_to_response("AgencyAdmin.html",{'uf':uf})
    def post(self, request):
        uf=UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            if username =='' or password =='':
                return render(request,"AgencyAdmin.html",{'uf':uf,"error":"用户名和密码不能为空"})
            ## 判断用户名与密码是否匹配
            users=User.objects.filter(username=username,password=password)
            if not users:
                 return render(request,"AgencyAdmin.html",{'uf':uf,"error":"用户名或密码错误"})
            user=users.first()
            if not user:
                return render(request,"AgencyAdmin.html",{'uf':uf,"error":"用户名或密码错误"})
            if user.audited==True:##登陆成功
                request.session['username']=username #将session信息写到服务器
                return HttpResponseRedirect('/agency/index/')
            else:
                return render_to_response("AgencyAdmin.html",{'uf':uf,'error':"等待审核"})
        else:
            uf=UserForm()
            return render_to_response("AgencyAdmin.html",{'uf':uf,'error':"错误"})
'''

class AgencyInfo(View):
    def post(self,request):
        util=Util()
        username=util.check_user(request)
        user_list=get_object_or_404(User,username=username)
        return render(request,"AgencyInfo.html",{"user_info":user_list})


# class TeacherLogin(View):
#     '''个人教师登陆,注册界面，如果存在账户则登陆，不存在则跳转到注册界面'''
#     def post(self, request):
#         uf=UserTForm(request.POST)
#         if uf.is_valid():
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             if username =='' or password =='':
#                 return render(request,"TeacherLogin.html",{'uf':uf,"error":"用户名和密码不能为空"})
#             ## 判断用户名与密码是否匹配 
#             user=User.objects.filter(username=username,password=password,privilege=2,audited=True)
#             if user:  ##登陆成功
#                 response = HttpResponseRedirect('/agency/index/')
#                 request.session['username']=username #将session信息写到服务器
#                 return response
#             else:
#                 return render(request,"AgencyLogin.html",{'uf':uf,"error":"用户名或密码错误"})
#         else:
#             uf=UserTForm()
#         return render_to_response("AgencyAdmin.html",{'uf':uf})


class AgencyLogout(View):
    #用户登出
    def get(self,request):
        response = HttpResponseRedirect('/index/') #登出后跳转到首页
        request.session['username']=""
        return response
    def post(self,request):
        self.get(request)
    



class AgencyRegister(View):
    # 教育机构注册
    def get(self,request):
        uf=UserAForm()
        return render_to_response('agency/AgencyRegister.html',{'uf':uf})
    def post(self, request):
        ## 用户提交注册表单
        uf=UserAForm(request.POST)
        if uf.is_valid():
            ##教育机构
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            email = (request.POST.get('email')).strip()
            field = (request.POST.get('field')).strip()
            idcode = (request.POST.get('idcode')).strip()
            address = (request.POST.get('address')).strip()
            intro = (request.POST.get('intro')).strip()
            aim_age = (request.POST.get('aim_age')).strip()
            phone = (request.POST.get('phone')).strip()
            user_list=User.objects.filter(username=username)
            if user_list:##用户已存在
                return render_to_response('agency/AgencyRegister.html',{'uf':uf,"error":"用户名已存在！"})
            else:
                user=User()
                applya=ApplyForm_a()
                user.username=username
                user.password=make_password(password)
                user.audited=False
                user.privilege=2
                user.save()  
                applya.username=username
                applya.email=email
                applya.idcode=idcode
                applya.field=field
                applya.address=address
                applya.intro =intro
                applya.phone = phone
                applya.aim_age = aim_age
                applya.save()
                return redirect('home')
        else:
            return render_to_response('agency/AgencyRegister.html',{'uf':uf,"error":"注册信息不完善"})
           


class TeacherRegister(View):
    # 个人教师用户注册
    def get(self,request):
        uf=UserTForm()
        return render_to_response('agency/TeacherRegister.html',{'uf':uf})
    def post(self, request):
        ## 用户提交注册表单
        uf=UserTForm(request.POST)
        if uf.is_valid():
            ##教育机构
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            email = (request.POST.get('email')).strip()
            field = (request.POST.get('field')).strip()
            name = (request.POST.get('name')).strip()
            sex = (request.POST.get('sex')).strip()
            address = (request.POST.get('address')).strip()
            intro = (request.POST.get('intro')).strip()
            aim_age = (request.POST.get('aim_age')).strip()
            phone = (request.POST.get('phone')).strip()
            idcard = (request.POST.get('idcard')).strip()
            user_list=User.objects.filter(username=username)
            if user_list:##用户已存在
                return render_to_response('agency/TeacherRegister.html',{'uf':uf,"error":"用户名已存在！"})
            else:
                user=User()
                user.username=username
                user.password=make_password(password)
                user.audited=False
                user.privilege=2
                user.save()  
                applya=ApplyForm_a()
                applya.username=user.username
                applya.email=email
                applya.idcard=idcard
                applya.field=field
                applya.address=address
                applya.save()
                return redirect('home')
        return render_to_response('agency/TeacherRegister.html',{'uf':uf,"error":"注册信息不完整！"})
                
            

class DisplayApply(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            uf=UserAForm()
            return render_to_response('Login.html',{'uf':uf,"error":"未登陆！"})
        else:
            apply_list=ListenApply.objects.all()
            return render(request,"agency/apply_list.html",{'apply_list':apply_list})




class DisplayNotice(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            next = request.GET.get('next', '/')
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'form': form, 'next':next})
        else:
            notice_list=Notice.objects.filter(username=username)
            return render(request,"agency/notice_list.html",{'notices':notice_list})
                
@ajax_required
@require_http_methods(["POST"])
def notice_delete(request):
    notice_id = request.POST['comment_id']
    instance = Notice.objects.get(notice_id=notice_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})           
            

                

class AddNotice(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            next = request.GET.get('next', '/')
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'form': form, 'next':next})
        else:
            form=NoticeAddForm()
            return render(request,"agency/notice_add.html",{'form':form,'username':username})

    def post(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            next = request.GET.get('next', '/')
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'form': form, 'next':next})
        else:
            ###Insert(Add)
            notice_item=NoticeAddForm(data=request.POST)
            newnotice=Notice()
            if notice_item.is_valid():
                newnotice.notice_content = (request.POST.get("notice_content")).strip()
                newnotice.notice_title = (request.POST.get("notice_title")).strip()
                newnotice.username=username 
                newnotice.save()
                user=User.objects.get(username=username)
                if user.privilege==2:
                    return redirect('/agency/teacher_index/')
                else:
                    return redirect('/agency/agency_index/')
            return render(self.request, 'agency/notice_add.html', {'form': notice_item}) 


        
class AddLesson(generic.CreateView):
    model = Lessons
    form_class = LessonPublishForm
    template_name = 'agency/lesson_add.html'
    success_url = '/agency/lesson_list/'


    
def lesson_detail(request,pk):
    util=Util()
    username=util.check_user(request)
    if username=='': ##未登录
        next = request.GET.get('next', '/')
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form': form, 'next':next})
    else:
        lesson=get_object_or_404(Lessons,lesson_id=pk)
        return render(request,'agency/detail.html',{"user":username,'lesson':lesson})

class LessonList(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            next = request.GET.get('next', '/')
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'form': form, 'next':next})
        else:
            lesson_list=Lessons.objects.all()
            return render(request,"agency/lesson_list.html",{'lesson_list':lesson_list})

class ApplyList(View):
    def get(self, request):
        util=Util()
        username=util.check_user(request)
        if username=='': ##未登录
            next = request.GET.get('next', '/')
            form = UserLoginForm()
            return render(request, 'registration/login.html', {'form': form, 'next':next})
        else:
            apply_list=ListenApply.objects.filter(username=username)
            return render(request,"agency/apply_list.html",{'apply_list':apply_list})


def change_price(request, pk):
    if request.method == 'POST':
        form = ChangePriceForm(request.POST)
        username=request.session.get('username')
        if form.is_valid():
            user=User.objects.get(username=username)
            lesson=Lessons.objects.get(lesson_id=pk)
            if not user.privilege==3:
                lesson.cprice=form.cleaned_data['new_price']
                lesson.save()
                request.session['username']=user.username  # 更新session 非常重要！
                return redirect('agency:lesson_list')
            else:
                messages.warning(request, '无权修改管理员密码')
                return redirect('agency:lesson_list')
        else:
            print(form.errors)
    else:
        form = ChangePriceForm()
        lesson=Lessons.objects.get(lesson_id=pk)
        price=lesson.cprice
    return render(request, 'agency/change_price.html', {
        'form': form,'id':price
    })



@ajax_required
@require_http_methods(["POST"])
def lesson_delete(request):
    notice_id = request.POST['comment_id']
    instance = Lessons.objects.get(lesson_id=notice_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})      