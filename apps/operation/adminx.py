# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/12 15:07'
import xadmin

from .models import UserAsk,UserCourse,UserMessage,CourseComments, UserFavourites

class UserAskAdmin(object):
    list_display = ['name',  'mobile','course_name','add_time']
    search_fields = ['name',  'mobile','course_name']
    list_filter = ['name',  'mobile','course_name','add_time']
class UserCourseAdmin(object):
    list_display = ['course', 'user', 'add_time']
    search_fields = ['course', 'user']
    list_filter = ['course__name', 'user__nick_name', 'add_time']

class UserMessgeAdmin(object):
    list_display = ['user', 'message', 'has_read','add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read','add_time']

class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']

class UserFavouritesAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessgeAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavourites,UserFavouritesAdmin)