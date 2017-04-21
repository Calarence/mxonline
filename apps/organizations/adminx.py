# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/12 14:40'

import xadmin

from .models import CityDict,Teacher,CourseOrg

class CityDictAdmin(object):
    list_display = ['name', 'add_time', 'desc']
    search_fields = ['name','desc']
    list_filter = ['name', 'add_time', 'desc']

class TeacherAdmin(object):
    list_display = ['org','name', 'work_years', 'work_company','work_position','points','click_num','fav_nums','add_time']
    search_fields = ['org','name', 'work_years', 'work_company','work_position','points','click_num','fav_nums']
    list_filter = ['org__name','name', 'work_years', 'work_company','work_position','points','click_num','fav_nums','add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'description', 'click_num','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'description', 'click_num','fav_nums','image','address','city']
    list_filter = ['name', 'description', 'click_num','fav_nums','image','address','city','add_time']
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)