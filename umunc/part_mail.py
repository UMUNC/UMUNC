#coding=utf-8
from django.core.mail import EmailMessage

def sendmail(to,subject,html):
	email = EmailMessage(
		subject= subject,
		body = html,
		to = [to])
	email.content_subtype = "html"
	email.send()

def sendmail_emailcheck(user):
	sendmail(user.email,u"UMUNC邮箱验证",u'''
		<style type="text/css">
			table {border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;}
			table * {border: 0px;}
			.text-center {text-align:center;}
			.head {background:#1C9EFF;color:white;padding:20px;}
			td {padding:20px;}
		</style>
		<table>
			<tr>
				<td class="text-center head">
					<h2>UMUNC邮箱验证</h2>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr>
				<td>
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此邮箱（ '''+user.email+u''' ）正在注册“UMUNC IRIS”的账号。</p>
					<p>如果这不是您的操作，请直接忽视本邮件；如果您确认这是您的操作，请点击下面的地址或将其复制到浏览器地址栏并进入，即可验证您的邮箱，激活账号：</p>
					<h4><a href=\"http://www.umunc.org/iris/accounts/check?checkcode='''+user.checkcode.CheckCode+u'''\">http://www.umunc.org/iris/accounts/check?checkcode='''+user.checkcode.CheckCode+u'''</a></h4>
				</td>
			</tr>
			<tr>
				<td class="text-center">
					<hr/>
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')

def sendmail_interview(user):
	sendmail(user.email,u"UMUNC面试通知",u'''
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
					<h3>UMUNC面试通知</h3>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr>
				<td>
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.username+u''' ）已经被核心学术团队分配了面试。</p>
					<p>您被分配的面试官为：</p>
					<h4><a href=\"http://www.umunc.org/iris/accounts/check?checkcode='''+user.username+u'''\">http://www.umunc.org/iris/accounts/check?checkcode='''+user.username+u'''</a></h4>
				</td>
			</tr>
			<tr>
				<td class="text-center">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
