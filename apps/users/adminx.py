# _*_ coding: utf-8 _*_
__author__ = 'Clarence'
__date__ = '2017/4/12 10:41'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
class GlobalSettings(object):
    site_title = "MxOnline"
    site_footer = "China UnionPay"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    site_footer = "测试"
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)