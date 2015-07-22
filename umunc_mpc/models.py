#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Press(models.Model):
	user = models.ManyToManyField(User,verbose_name="用户")
	name = models.CharField(max_length=255,verbose_name="名称")
	template = models.CharField(max_length=255,verbose_name="模板",blank=True)
	def __unicode__(self):
		return u'%s' % (self.name)

class Post(models.Model):
	title = models.CharField(max_length=255,verbose_name = '标题')
	content = models.TextField(verbose_name = "内容")
	author = models.ForeignKey(User,verbose_name = '作者')
	press = models.ManyToManyField(Press,verbose_name = '新闻社')
	timestamp = models.DateTimeField(auto_now=True, verbose_name = '时间戳')
	status=models.IntegerField(verbose_name='状态',choices=(
		(1,'草稿'),
		(2,'待审核'),
		(3,'待发布'),
		(4,'发布'),),)
	level=models.IntegerField(verbose_name="置顶")
	class Meta:
		ordering = ['status','-level','-timestamp']
	def __unicode__(self):
		return u'%s' % (self.title)