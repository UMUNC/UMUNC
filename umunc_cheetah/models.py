#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from umunc_iris.models import *

class room(models.Model):
	Name=models.CharField(max_length=255,blank=True,verbose_name="名称")
	User=models.ManyToManyField(User,verbose_name='用户')
	Block=models.BooleanField(default=False,verbose_name='禁言')
	class Meta:
		ordering = ['id']
	def __unicode__(self):
		return u'[%s] %s' % (self.id,self.Name)

class message(models.Model):
	FromU=models.ForeignKey(User,verbose_name='发送人')
	ToU=models.ForeignKey(room,verbose_name='接收房间')
	TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name='时间戳')
	System=models.BooleanField(default=False,verbose_name='系统消息')
	#Public=models.BooleanField(default=False,verbose_name='公共消息')
	Content=models.TextField(blank=True,verbose_name='内容')
	class Meta:
		ordering = ['-TimeStamp']
	def __unicode__(self):
		return u'%s[%s] %s' % (self.FromU,self.ToU.Name,self.TimeStamp)

class meeting(models.Model):
	FromC=models.ForeignKey(country,verbose_name='发起方',related_name='Sent_meeting')
	ToC=models.ForeignKey(country,verbose_name='接收方',related_name='Recived_meeting')
	Time=models.DateTimeField(verbose_name='时间')
	Location=models.CharField(max_length=255,blank=True,verbose_name="地点")
	Description=models.CharField(max_length=255,blank=True,verbose_name="说明")
	Check_F=models.NullBooleanField(default=None,verbose_name='发起者确认')
	Check_T=models.NullBooleanField(default=None,verbose_name='接受者确认')
	Check_A=models.NullBooleanField(default=None,verbose_name='管理员确认')
	Global=models.BooleanField(default=False,verbose_name='全局')
	class Meta:
		ordering = ['-id']
	@property
	def check_accept(self):
		if (self.Check_A and self.Check_T and self.Check_F)==True:
			return 'Accepted'
		elif (self.Check_A==False) or (self.Check_T==False) or (self.Check_F==False):
			return 'Rejected'
		return 'Waiting'
	def __unicode__(self):
		return u'%s-%s [%s]' % (self.FromC,self.ToC.Name,self.check_accept())
