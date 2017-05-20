# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/5/8 14:46'
from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UserCourseView,UserFavOrgView
from .views import UserFavTeachersView,UserFavCourseView,UserMessageView,LogoutView

urlpatterns = [
    url(r'^info/$',UserInfoView.as_view(),name="userInfo"),
    url(r'^imageUpload/$',UploadImageView.as_view(),name="uploadImage"),
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name="updatePwd"),
    url(r'^sendEmailCode/$',SendEmailCodeView.as_view(),name="sendEamil"),
    # url(r'^updateUserEmail/$',)
    url(r'^userCourse/$',UserCourseView.as_view(),name="userCourse"),
    url(r'userFavOrg/$',UserFavOrgView.as_view(),name="userFavOrg"),
    url(r'^userFavTeacher/$',UserFavTeachersView.as_view(),name="userFavTeacher"),
    url(r'^userFavCourse/$',UserFavCourseView.as_view(),name="userFavCourse"),
    url(r'^userMessage/$',UserMessageView.as_view(),name="userMessage"),
    url(r'^logout/$',LogoutView.as_view(),name="logout")


]