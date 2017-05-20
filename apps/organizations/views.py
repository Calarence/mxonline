# encoding: utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CourseOrg, CityDict,Teacher
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavourites


# Create your views here.
class OrgView(View):
    def get(self, request):
        allOrganizations = CourseOrg.objects.all()
        keywords = request.GET.get("keywords","")
        if keywords:
            allOrganizations = allOrganizations.filter(name__icontains=keywords)
        hotOrganizations = allOrganizations.order_by("-click_num")[:3]
        allCities = CityDict.objects.all()
        cityId = request.GET.get("city", "")
        ct = request.GET.get("ct", "")
        sort = request.GET.get("sort", "")

        if cityId:
            allOrganizations = allOrganizations.filter(city=cityId)
        if ct:
            allOrganizations = allOrganizations.filter(category=ct)
        orgCount = allOrganizations.count()
        if sort == 'students':
            allOrganizations = allOrganizations.order_by("-students")
        elif sort == 'courseNums':
            allOrganizations = allOrganizations.order_by("-courseNums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(allOrganizations, 1, request=request)

        allOrganizations = p.page(page)

        # return render_to_response('index.html', {
        #     'allOrganizations': allOrganizations
        # })
        return render(request, 'org-list.html', {
            'allOrganizations': allOrganizations,
            'allCities': allCities,
            'orgCount': orgCount,
            'cityId': cityId,
            'ct': ct,
            "hotOrganizations": hotOrganizations,
            "sort": sort
        })


class AddUserAskView(View):
    def post(self, request):
        print request.POST.get("name")
        userAskForm = UserAskForm(request.POST)
        if userAskForm.is_valid():
            userAskForm.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    def get(self, request, org_id):
        currentPage = 'home'
        hasFav = False
        if request.user.is_authenticated():
            if UserFavourites.objects.filter(user=request.user,fav_id=org_id,fav_type=2):
                hasFav = True
        organization = CourseOrg.objects.get(id=int(org_id))
        allCourses = organization.course_set.all()[:3]
        allTeachers = organization.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html',
                      {'organization': organization, 'allCourses': allCourses, 'allTeachers': allTeachers,
                       'org_id': org_id,'currentPage':currentPage,'hasFav':hasFav})


class OrgCourseView(View):
    def get(self, request, org_id):
        # print org_id
        currentPage = 'course'
        organization = CourseOrg.objects.get(id=int(org_id))
        hasFav = False
        if request.user.is_authenticated():
            if UserFavourites.objects.filter(user=request.user, fav_id=org_id, fav_type=1):
                hasFav = True
        all_courses = organization.course_set.all()
        return render(request, 'org-detail-course.html',
                      {'organization': organization, 'all_courses': all_courses, 'currentPage': currentPage,'hasFav':hasFav})

class OrgDescView(View):
    def get(self,request,org_id):
        hasFav = False
        if request.user.is_authenticated():
            if UserFavourites.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                hasFav = True
        organization = CourseOrg.objects.get(id=int(org_id))
        currentPage = 'desc'
        return render(request,'org-detail-desc.html',{'organization':organization,'currentPage':currentPage,'hasFav':hasFav})
class OrgTeacherView(View):
    def get(self,request,org_id):
        hasFav = False
        if request.user.is_authenticated():
            if UserFavourites.objects.filter(user=request.user, fav_id=org_id, fav_type=3):
                hasFav = True
        organization = CourseOrg.objects.get(id=int(org_id))
        teachers = organization.teacher_set.all()
        currentPage = 'teacher'
        return render(request,'org-detail-teachers.html',{'currentPage':currentPage,'teachers':teachers,'organization':organization,'hasFav':hasFav})

class AddFavouriteView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            print ("未登录")
            return  HttpResponse('{"status":"fail","msg":"用户未登陆"}', content_type='application/json')
        else:
            favId = int(request.POST.get('fav_id', ''))
            favType = int(request.POST.get('fav_type', ''))
            existRecords = UserFavourites.objects.filter(user=request.user,fav_id=favId,fav_type=favType)
            if existRecords:
                existRecords.delete()
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                if favId > 0 and favType > 0:
                    userFavourite = UserFavourites()
                    userFavourite.fav_id = favId
                    userFavourite.fav_type = favType
                    userFavourite.user = request.user
                    userFavourite.save()
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    def get(self,request):
        allTeachers = Teacher.objects.all()
        sort = request.GET.get("sort","")
        keywords = request.GET.get("keywords","")
        if keywords:
            allTeachers = allTeachers.filter(name__icontains=keywords)
        if sort:
            if sort == "hot":
                allTeachers = allTeachers.order_by("-click_num")
        sortedTeachers = Teacher.objects.all().order_by("-click_num")[:3]
        count = allTeachers.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(allTeachers, 1, request=request)

        allTeachers = p.page(page)
        return render(request,'teachers-list.html',{"allTeachers":allTeachers,"count":count,
                                                    "sortedTeachers":sortedTeachers,"sort":sort})

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        allCourses = Course.objects.all().filter(teacher=teacher)
        org = teacher.org
        sortedTeachers = Teacher.objects.all().order_by("-click_num")[:3]
        return render(request,'teacher-detail.html',{"teacher":teacher,"allCourses":allCourses,"sortedTeachers":sortedTeachers,"org":org})