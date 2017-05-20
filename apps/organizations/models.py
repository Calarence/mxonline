#encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name="城市")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")
    desc = models.CharField(max_length=200,verbose_name="描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name="机构名称")
    description = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20,choices=(('pxjg',"培训机构"),("gr","个人"),("gx","高效")),default="pxjg",verbose_name="机构类型")
    click_num = models.IntegerField(default=0,verbose_name="点击数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    students = models.IntegerField(default=0,verbose_name="学习人数")
    courseNums = models.IntegerField(default=0,verbose_name="课程数")
    image = models.ImageField(upload_to="org/%Y/%m",verbose_name="Logo")
    address = models.CharField(max_length=150,verbose_name="机构地址")
    city  = models.ForeignKey(CityDict,verbose_name="所在城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def getTeacherNums(self):
        allTeachers = self.teacher_set.all()
        return allTeachers.count()

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name="所属机构")
    name = models.CharField(max_length=50,verbose_name="教师名称")
    work_years = models.IntegerField(default=0)
    work_company = models.CharField(max_length=50,verbose_name="就职公司")
    work_position = models.CharField(verbose_name="公司职位",max_length=50)
    points = models.CharField(verbose_name="教学特点",max_length=50)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="teacher/%Y/%m",verbose_name="教师头像",default="")
    add_time = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

