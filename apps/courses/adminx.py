# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/12 14:16'
import xadmin


from .models import Course,CourseResource,Lesson,Video

class CourseAdmin(object):
    list_display = ['name', 'description', 'detail', 'degree', 'learn_times', 'students', 'favourites', 'image',
                    'click_nums', 'add_time']
    search_fields = ['name', 'description', 'detail', 'degree', 'learn_times', 'students', 'favourites', 'image',
                    'click_nums']
    list_filter = ['name', 'description', 'detail', 'degree', 'learn_times', 'students', 'favourites', 'image',
                    'click_nums', 'add_time']
class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['name']
    list_filter = ['course__name','name','add_time']

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['name']
    list_filter = ['lesson__name', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time','download']
    search_fields = ['name']
    list_filter = ['course', 'name', 'add_time','download']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)