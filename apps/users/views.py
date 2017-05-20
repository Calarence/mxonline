# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile, EmailVerifyRecord,Banner
from django.views.generic.base import View
from organizations.models import Teacher
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import sendRegisterEmail
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UploadImageForm
from operation.models import UserCourse,UserFavourites,UserMessage
from organizations.models import CourseOrg
from courses.models import Course
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):

    def get(self, request):
        registerForm = RegisterForm()
        return render(request, "register.html", {"registerForm": registerForm})

    def post(self, request):
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user = UserProfile()
            username = request.POST.get("email", "")
            if UserProfile.objects.filter(email=username):
                return render(request, "register.html", {"msg": "用户已经存在", "registerForm": registerForm})
            password = request.POST.get("password")
            user.username = username
            user.email = username
            user.password = make_password(password)
            user.is_active = False
            user.save()
            sendRegisterEmail(username, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"registerForm": registerForm})


class LoginView(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


def userLogin(request):
    if request.method == 'GET':
        return render(request, "login.html", {})
    else:
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})


class ActiveUserView(View):

    def get(self, request, active_code):
        allRecords = EmailVerifyRecord.objects.filter(code=active_code)
        if allRecords:
            for record in allRecords:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPasswordView(View):

    def get(self, request):
        forgetForm = ForgetForm()
        return render(request, 'forgetpwd.html', {"forgetForm": forgetForm})

    def post(self, request):
        forgetForm = ForgetForm(request.POST)
        if forgetForm.is_valid():
            email = request.POST.get("email", "")
            sendRegisterEmail(email, send_type="forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetForm": forgetForm})


class ResetView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "reset_fail.html")


class ModifyPwdView(View):

    def post(self, request):
        modifyPwdForm = ModifyPwdForm(request.POST)
        if modifyPwdForm.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"msg": "密码不一致"})
            else:
                user = UserProfile.objects.get(email=email)
                password = make_password(pwd1)
                user.password = password
                user.save()
                return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modifyPwdForm": modifyPwdForm})


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'usercenter-info.html')


class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):

    def post(self, request):
        modifyForm = ModifyPwdForm(request.POST)
        res = dict()
        if modifyForm.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '两次密码不一致'
                return HttpResponse(json.dumps(res), content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            res['status'] = 'success'
            res['msg'] = '密码修改成功'
        else:
            res = modifyForm.errors

        return HttpResponse(json.dumps(res), content_type="application/json")


class SendEmailCodeView(LoginRequiredMixin, View):

    def get(self, request):
        email = request.GET.get("email", "")
        res = {}
        if UserProfile.objects.all().filter(email=email):
            res["status"] = "fail"
            res["msg"] = "该邮箱已经注册"
            return HttpResponse(json.dumps(res), content_type="application/json")
        sendRegisterEmail(email, "sendEmailCode")
        res["status"] = "success"
        res["msg"] = "发送成功"
        return HttpResponse(json.dumps(res), content_type="application/json")


class UpdateUserEmail(LoginRequiredMixin, View):

    def post(self, request):
        res = {}
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        record = EmailVerifyRecord.objects.all().filter(
            email=email, code=code, send_type="sendEmailCode")
        if record:
            user = request.user
            user.email = email
            user.save()
            res['status'] = 'success'
            res['msg'] = '邮箱修改成功！'
        else:
            res["status"] = "fail"
            res["msg"] = "验证码出错"
        return HttpResponse(json.dumps(res), content_type="application/json")

class UserCourseView(LoginRequiredMixin,View):
    def get(self,request):
        userCourses = UserCourse.objects.all().filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{"userCourses":userCourses})


class UserFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list = []
        favOrgs = UserFavourites.objects.all().filter(user=request.user,fav_type=2)
        for favOrg in favOrgs:
            orgId = favOrg.fav_id
            print orgId
            org = CourseOrg.objects.get(id=orgId)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{"org_list":org_list})

class UserFavTeachersView(LoginRequiredMixin,View):
    def get(self,request):
        favTeachers = []
        fav_teachers = UserFavourites.objects.all().filter(user=request.user,fav_type=3)
        for favTeacher in fav_teachers:
            teacherId = favTeacher.fav_id
            teacher = Teacher.objects.get(id=teacherId)
            favTeachers.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{"favTeachers":favTeachers})

class UserFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        favCourses = []
        fav_courses = UserFavourites.objects.all().filter(user=request.user,fav_type=1)
        for favCourse in fav_courses:
            courseId = favCourse.fav_id
            course = Course.objects.get(id=courseId)
            favCourses.append(course)
        return render(request,'usercenter-fav-course.html',{"favCourses":favCourses})
class UserMessageView(LoginRequiredMixin,View):
    def get(self,request):
        allMessages = UserMessage.objects.all().filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(allMessages, 1, request=request)

        messages = p.page(page)
        return render(request,'usercenter-message.html',{"messages":messages})

# 用户登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return  HttpResponseRedirect(reverse("index"))

class IndexView(View):
    def get(self,request):
        allBanners = Banner.objects.all().order_by('index')
        courses = Course.objects.all().filter(isBanner=False)[:5]
        bannerCourses = Course.objects.all().filter(isBanner=True)[:3]
        courseOrgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{"allBanners":allBanners,"courses":courses,"bannerCourses":bannerCourses,"courseOrgs":courseOrgs})

def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

    # 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response