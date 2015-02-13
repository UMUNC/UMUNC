#coding=utf-8
from django.core.mail import EmailMessage

register={
	'HOST':"smtp.163.com",
	'PORT':25,
	'MAIL':"eastpiger@163.com",
	'PASSWORD':"Lazarus19950408",}

def sendmail(sender,to,subject,html):
	email = EmailMessage(subject, html, 'umunc_register@eastpiger.com', [to])
	email.content_subtype = "html"
	email.send()

def sendmail_emailcheck(to,username,code):
	sendmail(register,to,username+u"，快来验证您的邮箱吧！",u"<h3>尊敬的用户 "+username+u" 您好：</h3><p>您收到此邮件是因为此邮箱（ "+to+u" ）正在注册“UMUNC IRIS”的账号。</p><p>如果这不是您的操作，请直接忽视本邮件；如果您确认这是您的操作，请点击下面的地址或将其复制到浏览器地址栏并进入，即可验证您的邮箱，激活您的账号：</p><h4><a href=\"http://121.41.24.81/iris/accounts/check?checkcode="+code+u"\">http://121.41.24.81/iris/accounts/check?checkcode="+code+u"</a></h4><br/><p><small>建议您尽早激活。<br/>如果您未找到激活邮件，请查看是否被识别为垃圾邮件，或尝试更换邮箱和重发链接。</small></p><hr/><p>UMUNC</p>")