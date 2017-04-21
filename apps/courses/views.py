from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
class CourseListView(View):
    def get(self,request):
        allCourses = Course.objects.all().order_by("-add_time")
        hotCourses = Course.objects.all().order_by("-click_nums")[:3]
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