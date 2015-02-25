#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class group(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	School=models.CharField(max_length=255,verbose_name="在读学校")
	Password=models.CharField(max_length=255,verbose_name="口令")
	Payment=models.BooleanField(default=False,verbose_name=' 缴费')
	Group=models.BooleanField(default=False,verbose_name=' 集体团队/个人团队')
	class Meta:
		ordering = ['-id']
	def __unicode__(self):
		return u'%s - %s' % (self.Name,self.Payment)
	
class country(models.Model):
	Name=models.CharField(max_length=255,verbose_name="名称")
	class Meta:
		ordering = ['id']
	def __unicode__(self):
		return u'%s' % (self.Name)

class profile(models.Model):
	User=models.OneToOneField(User,verbose_name='账户')
	Init=models.BooleanField(default=False,verbose_name='初始化')
	Group=models.ForeignKey(group,blank=True,null=True,verbose_name='团队')
	Leader=models.BooleanField(default=False,verbose_name=' 领队')
	Name=models.CharField(max_length=255,blank=True,verbose_name="姓名")
	Sex=models.BooleanField(default=False,verbose_name='性别')
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
	MunJoined=models.BooleanField(default=False,verbose_name='参与过UMUNC')
	MunJoinedC=models.CharField(max_length=255,verbose_name="参与过的UMUNC会议",blank=True)
	Commitee=models.IntegerField(verbose_name='志愿',choices=(
		('西南',(
				(1,'联动体系 - 国家内阁'),
				(2,'联动体系 - 联合国安全理事会'),
				(3,'联动体系 - 主新闻中心'),
				(4,'联动体系 - 联合国秘书处'),
				(5,'欧洲体系 - 欧盟委员会'),
				(6,'欧洲体系 - 欧盟理事会'),
				(7,'GAUS - United Security Council'),
				(8,'GAUS - United Nations General Assembly 1st Committee - Disarmament and International Security Committee'),
				(9,'独立会场 - 世界旅游旅行大会'),
			)
		),
		('西北',(
				(10,'联动体系 - 国家内阁'),
				(11,'联动体系 - 东盟10+3峰会'),
				(12,'联动体系 - 主新闻中心'),
				(13,'联动体系 - 联合国秘书处'),
				(14,'独立会场 - 欧洲安全与合作组织部长级会议'),
				(15,'Independent Committee - United Nations General Assembly 1st Committee - Disarmament and International Security Committee'),
			)
		),
		('华北',(
				(16,'联动体系 - 国家内阁'),
				(17,'联动体系 - 联合国安全理事会'),
				(18,'联动体系 - 主新闻中心'),
				(19,'联动体系 - 联合国秘书处'),
				(20,'独立会场 - 联合国开发计划署'),
				(21,'Independent Committee - United Nations General Assembly 3rd Committee - Social, Humanitarian and Culture Committee'),
			)
		),))
	Country=models.ForeignKey(country,verbose_name="席位-所属国家",null=True,blank=True)
	Identify=models.CharField(max_length=255,verbose_name="席位-席位名称",blank=True)
	TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name='时间戳')
	Status=models.IntegerField(verbose_name='状态',choices=(
		(-3,'代表申请拒绝'),
		(0,'未验证邮箱'),
		(1,'等待提交代表申请'),
		(2,'代表申请已提交'),
		(3,'代表申请已通过，等待确认团队'),
		(4,'团队已确认，等待提交学术评测'),
		(5,'学术评测已提交'),))
	class Meta:
		ordering = ['id']
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

class review(models.Model):
	User=models.OneToOneField(User,verbose_name='账户')
	TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name='时间戳')
	Content=models.TextField(verbose_name='内容')
	class Meta:
		ordering = ['TimeStamp']
	def __unicode__(self):
		return u'%s %s' % (self.TimeStamp,self.User.username)
