# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/21 9:06'

from django.conf.urls import url
from .views import CourseListView



urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name="courseList")
    # url(r'^add_ask/$',AddUserAskView.as_view(),name="addUserAsk"),
    # url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name="home"),
    # url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name="orgCourse"),
    # url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name="orgDesc"),
    # url(r'^orgteacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name="orgTeacher"),
    # url(r'^add_fav/$',AddFavouriteView.as_view(),name="addFav")



]