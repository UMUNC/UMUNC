#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

import simplejson
from umunc.settings import COMMITEE_DIR, COMMITEE_DIR2

def load_commitee():
	destination = open(COMMITEE_DIR,'r')
	t=destination.read()
	destination.close()
	return simplejson.loads(t)

def load_commitee2():
	destination = open(COMMITEE_DIR2,'r')
	t=destination.read()
	destination.close()
	return simplejson.loads(t)

class group(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	School=models.CharField(max_length=255,verbose_name="在读学校")
	Password=models.CharField(max_length=255,verbose_name="口令")
	Paycode=models.CharField(max_length=255,verbose_name="缴费密钥")
	Payment=models.BooleanField(default=False,verbose_name='缴费')
	Group=models.BooleanField(default=False,verbose_name='集体团队/个人团队',choices=(
		(True,'集体团队'),
		(False,'个人团队'),))
	class Meta:
		ordering = ['-id']
	def __unicode__(self):
		return u'%s' % (self.Name)

class system(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	class Meta:
		ordering = ['id']
	def __unicode__(self):
		return u'%s' % (self.Name)

class country(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	System=models.ForeignKey(system,verbose_name='所属体系',null=True,blank=True)
	class Meta:
		ordering = ['id']
	def __unicode__(self):
		return u'%s-%s' % (self.System, self.Name)

class identify(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	Country=models.ForeignKey(country,verbose_name='所属国家',null=True,blank=True)
	class Meta:
		ordering = ['id']
	def __unicode__(self):
		return u'%s-%s' % (self.Country, self.Name)

class profile(models.Model):
	Interviewer=models.ForeignKey(User,verbose_name='面试官',null=True,blank=True,related_name='Interviewee')
	User=models.OneToOneField(User,verbose_name='账户')
	Init=models.BooleanField(default=False,verbose_name='初始化？',choices=(
		(True,'是'),
		(False,'否'),))
	Group=models.ForeignKey(group,blank=True,null=True,verbose_name='团队')
	Leader=models.BooleanField(default=False,verbose_name='领队？',choices=(
		(True,'首席代表'),
		(False,'非首席代表'),))
	Name=models.CharField(max_length=255,blank=True,verbose_name="姓名")
	Sex=models.BooleanField(default=False,verbose_name='性别',choices=(
		(True,'男'),
		(False,'女'),))
	Age=models.IntegerField(verbose_name='年龄')
	IDNum=models.CharField(max_length=18,verbose_name='身份证号',blank=True)
	School=models.CharField(max_length=255,verbose_name="在读学校",blank=True)
	Grade=models.IntegerField(verbose_name='在读年级',choices=(
		(1,'初中及以下 Middle school and under'),
		(2,'高一 Grade 10'),
		(3,'高二 Grade 11'),
		(4,'高三 Grade 12'),
		(5,'间隔年 Gap Year'),
		(6,'大学及以上 College and above'),))
	GName=models.CharField(max_length=255,verbose_name="监护人姓名",blank=True)
	GPhone=models.CharField(max_length=255,verbose_name="监护人电话",blank=True)
	Phone=models.CharField(max_length=255,verbose_name="联系电话",blank=True)
	Phone2=models.CharField(max_length=255,verbose_name="备用电话",blank=True)
	QQ=models.CharField(max_length=255,verbose_name="QQ",blank=True)
	Wechat=models.CharField(max_length=255,verbose_name="Wechat",blank=True)
	MunAge=models.IntegerField(verbose_name='模联年龄')
	MunRsm=models.TextField(verbose_name='模联经历',blank=True)
	Commitee=models.IntegerField(verbose_name='志愿',choices=load_commitee())
	Commitee2=models.IntegerField(verbose_name='志愿',choices=load_commitee2())
	Adjust=models.BooleanField(default=False,verbose_name='接受调剂？',choices=(
		(True,'是'),
		(False,'否'),))
	Identify=models.OneToOneField(identify,verbose_name="席位-席位名称",null=True,blank=True)
	TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name='注册时间戳')
	LastMotified=models.DateTimeField(auto_now=True,verbose_name='修改时间戳')
	Review1=models.TextField(verbose_name='学术评测T1',blank=True)
	Review2=models.TextField(verbose_name='学术评测T2',blank=True)
	Review3=models.TextField(verbose_name='学术评测T3',blank=True)
	Review4=models.TextField(verbose_name='学术评测T4',blank=True)
	Comment=models.TextField(verbose_name='学团评价',blank=True)
	Status=models.IntegerField(verbose_name='状态',choices=(
		(-3,'代表申请拒绝'),
		(-4,'代表退会'),
		(0,'未验证邮箱'),
		(1,'等待提交代表信息'),
		(2,'代表信息已提交，请确认团队信息'),
		(3,'代表团队已提交，请提交学术评测'),
		(4,'代表学测已提交，请等待分配面试'),
		(5,'代表面试已分配，请准备面试'),
		(6,'代表面试已通过，等待分配席位'),
		(7,'代表席位已分配，请进行缴费'),
		(8,'代表缴费已完成，申请完成'),))
	class Meta:
		ordering = ['-LastMotified']
		permissions = (
			("control_all", "Can Control All Data"),
		)
	def __unicode__(self):
		return u'[%s] %s' % (self.User.username,self.Name)

class checkcode(models.Model):
	User=models.OneToOneField(User,verbose_name='账户')
	CheckCode=models.CharField(max_length=255,verbose_name='验证码')
	TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name='时间戳')
	class Meta:
		ordering = ['-TimeStamp']
	def __unicode__(self):
		return u'[%s] %s' % (self.User.id,self.User.username)
