#encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from .models import Course,CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavourites,CourseComments,UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
class CourseListView(View):
    def get(self,request):
        allCourses = Course.objects.all().order_by("-add_time")
        hotCourses = Course.objects.all().order_by("-click_nums")[:3]
        keywords = request.GET.get("keywords","")
        if keywords:
            allCourses = allCourses.filter(Q(name__icontains=keywords)|Q(detail__icontains=keywords)|Q(description__icontains=keywords))
        sort = request.GET.get("sort", "")
        if sort == 'students':
            allCourses = allCourses.order_by("-students")
        elif sort == 'hot':
            allCourses = allCourses.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(allCourses, 1, request=request)

        allCourses = p.page(page)
        return render(request,'course-list.html',{"allCourses":allCourses,"sort":sort,'hotCourses':hotCourses})

class CourseDetailView(View):
    def get(self,request,course_id):
        hasFavourtieCourse = False
        hasFavourtieOrg = False
        if request.user.is_authenticated:
            if UserFavourites.objects.filter(user=request.user,fav_id=course_id):
                hasFavourtieCourse = True
            if UserFavourites.objects.filter(user=request.user,fav_id=2):
                hasFavourtieOrg = True

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if  tag:
            relatedCourse = Course.objects.filter(tag=tag)
        else:
            relatedCourse = []
        return render(request,'course-detail.html',{"course":course,"relatedCourse":relatedCourse,
                                                    "hasFavourtieCourse":hasFavourtieCourse,"hasFavourtieOrg":hasFavourtieOrg})

class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        userCourse = UserCourse.objects.filter(course=course)
        if not userCourse:
            userCourse = UserCourse(user=request.user,course=course)
            userCourse.save()
        userCouses = UserCourse.objects.filter(course=course)
        userIds = [userCourse.user.id for userCourse in userCouses]
        all_user_courses = UserCourse.objects.filter(user_id__in=userIds)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids)
        allLessons = course.get_lessons()
        allResources = CourseResource.objects.all().filter(course=course)
        return render(request,'course-video.html',{"course":course,"allLessons":allLessons,"allResources":allResources,"related_courses":related_courses})
class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        userCouses = UserCourse.objects.filter(course=course)
        userIds = [userCourse.user.id for userCourse in userCouses]
        all_user_courses = UserCourse.objects.filter(user_id__in=userIds)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids)
        comments = course.coursecomments_set.all()
        return render(request,'course-comment.html',{"course":course,"comments":comments,"related_courses":related_courses})

class AddCourseCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        else:
            couseId = request.POST.get("courseId",0)
            comments = request.POST.get("comment","")
            if couseId > 0 and comments:
                course = Course.objects.get(id=int(couseId))
                courseComment = CourseComments()
                courseComment.course =  course
                courseComment.user = request.user
                courseComment.comments = comments
                courseComment.save()
                return HttpResponse('{"status":"success"，"msg":"添加成功}',content_type='application/json')
            else:
                return HttpResponse({"status":"fail","msg":"添加失败"},content_type='application/json')
