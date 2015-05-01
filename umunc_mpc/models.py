#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255,verbose_name = '名称')

class Post(models.Model):
    title = models.CharField(max_length=255,verbose_name = '标题')
    content = models.TextField(verbose_name = "内容")
    author = models.ForeignKey(User,verbose_name = '作者')
    status = models.BooleanField(verbose_name = '审核')
    tag = models.ManyToManyField(Tag,verbose_name = '标签')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name = '时间戳')
    class Meta:
        ordering = ['-timestamp']