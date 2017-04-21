# encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organizations.models import CourseOrg


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",null=True)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    description = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), default="cj", max_length=10,verbose_name="难度")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    favourites = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程信息")
    name = models.CharField(verbose_name="章节名称", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(verbose_name="视频名称", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频信息"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(verbose_name="资源名称", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="下载地址")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
