#coding=utf-8
from django.core.mail import EmailMessage

def sendmail(to,subject,html):
	email = EmailMessage(
		subject= subject,
		body = html,
		to = [to])
	email.content_subtype = "html"
	email.send()

def sendmail_emailcheck(to,username,code):
	sendmail(to,u"UMUNC邮箱验证",u'''
		<style type="text/css">
			table {border: 0px;}
			table * {border: 0px;}
			.text-center {align:center;}
			.head {background:#1C9EFF;color:white;}
			tr {padding:20px;}
		</style>
		<table>
			<tr>
				<td class="text-center head">
					<h3>UMUNC邮箱验证</h3>
					<span>'''+username+u'''</span>
				</td>
			</tr>
			<tr>
				<td>
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此邮箱（ '''+to+u''' ）正在注册“UMUNC IRIS”的账号。</p>
					<p>如果这不是您的操作，请直接忽视本邮件；如果您确认这是您的操作，请点击下面的地址或将其复制到浏览器地址栏并进入，即可验证您的邮箱，激活账号：</p>
					<h4><a href=\"http://www.umunc.org/iris/accounts/check?checkcode='''+code+u'''\">http://www.umunc.org/iris/accounts/check?checkcode='''+code+u'''</a></h4>
				</td>
			</tr>
			<tr>
				<td class="text-center">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
