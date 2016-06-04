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
	# try:
	sendmail(user.email,u"UMUNC邮箱验证",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;">
					<h2 style="border:0px;padding:0px;margin:0px;">UMUNC邮箱验证</h2>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此邮箱（ '''+user.email+u''' ）正在注册“UMUNC IRIS”的账号。</p>
					<p>如果这不是您的操作，请直接忽视本邮件；如果您确认这是您的操作，请点击下面的地址或将其复制到浏览器地址栏并进入，即可验证您的邮箱，激活账号：</p>
					<h4><a href=\"http://www.umunc.org/iris/accounts/check?checkcode='''+user.checkcode.CheckCode+u'''\">http://www.umunc.org/iris/accounts/check?checkcode='''+user.checkcode.CheckCode+u'''</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;">
					<hr/>
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	# except:
	# 	pass

def sendmail_interviewer(user):
	# try:
	sendmail(user.profile.Interviewer.email,u"UMUNC面试安排通知",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;" colspan="2">
					<h3>UMUNC面试安排通知</h3>
					<span>'''+user.profile.Interviewer.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.profile.Interviewer.username+u''' ）已经被核心学术团队分配了面试。身为面试官的您被分配的面试者为：</p>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:right;">
					面试者：<br/>
					联系电话：<br/>
					电子邮箱：
				</td>
				<td style="padding:20px;text-align:left;">
				'''+user.profile.Name+u'''<br/>
				'''+user.profile.Phone+u'''<br/>
				'''+user.email+u'''
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>不用我说了自己联系被面试者单撸吧，安排结果记得尽快登记到系统后台并通知核心学术团队呦。</p>
					<p>详细信息：</p>
					<h4><a href=\"http://www.umunc.org/admin/\">http://www.umunc.org/admin/</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;" colspan="2">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	# except:
	# 	pass

def sendmail_interview(user):
	# try:
	sendmail(user.email,u"UMUNC面试通知",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;" colspan="2">
					<h3>UMUNC面试通知</h3>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.username+u''' ）已经被核心学术团队分配了面试。您被分配的面试官为：</p>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:right;">
					面试官：<br/>
					联系电话：<br/>
					电子邮箱：
				</td>
				<td style="padding:20px;text-align:left;">
				'''+user.profile.Interviewer.profile.Name+u'''<br/>
				'''+user.profile.Interviewer.profile.Phone+u'''<br/>
				'''+user.profile.Interviewer.email+u'''
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>请等待学术团队与您取得联系,如果在面试方式与时间上有任何问题，请与您当前的面试官取得联系。</p>
					<p>详细信息：</p>
					<h4><a href=\"http://www.umunc.org/iris/step4/\">http://www.umunc.org/iris/step4/</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;" colspan="2">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	sendmail_interviewer(user)
	# except:
	# 	pass

def sendmail_interview_reject(user):
	# try:
	sendmail(user.email,u"UMUNC面试结果通知",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;" colspan="2">
					<h3>UMUNC面试结果通知</h3>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.username+u''' ）已经被核心学术团队分配了面试。但是抱歉，经过我们对您的面试以及学测的审阅，我们认为您更加适合其他的席位，因此，我们为您重新安排了面试官。您的新面试官是：</p>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:right;">
					面试官：<br/>
					联系电话：<br/>
					电子邮箱：
				</td>
				<td style="padding:20px;text-align:left;">
				'''+user.profile.Interviewer.profile.Name+u'''<br/>
				'''+user.profile.Interviewer.profile.Phone+u'''<br/>
				'''+user.profile.Interviewer.email+u'''
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>请等待学术团队与您取得联系,如果在面试方式与时间上有任何问题，请与您当前的面试官取得联系。</p>
					<p>详细信息：</p>
					<h4><a href=\"http://www.umunc.org/iris/step4/\">http://www.umunc.org/iris/step4/</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;" colspan="2">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	sendmail_interviewer(user)
	# except:
	# 	pass

def sendmail_identify(user):
	# try:
	sendmail(user.email,u"UMUNC席位分配通知",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;" colspan="2">
					<h3>UMUNC席位分配通知</h3>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.username+u''' ）已经被核心学术团队分配了席位。您被分配的席位为：</p>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:right;">
					席位：<br/>
				</td>
				<td style="padding:20px;text-align:left;">
				'''+user.profile.Identify+u'''
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>您现在可以准备进行缴费了。</p>
					<p>详细信息：</p>
					<h4><a href=\"http://www.umunc.org/iris/step5/\">http://www.umunc.org/iris/step5/</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;" colspan="2">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	# except:
	# 	pass

def sendmail_payment_user(user):
	# try:
	sendmail(user.email,u"UMUNC缴费确认通知",u'''
		<table style="border-radius: 3px;border: 1px solid #d8d8d8;border-bottom-width: 2px;border-top-width: 0;">
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center; background:#1C9EFF;color:white;padding:20px;" colspan="2">
					<h3>UMUNC缴费确认通知</h3>
					<span>'''+user.username+u'''</span>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;" colspan="2">
					<p>致 与众不同的你：</p>
					<p>您收到此邮件是因为此账号（ '''+user.username+u''' ）所在团队已经核实完成了缴费流程。</p>
					<p>请注意，报名成功的前提是完成缴费和完成报名流程，详细情况可以到这里确认：</p>
					<h4><a href=\"http://www.umunc.org/iris/\">http://www.umunc.org/iris/</a></h4>
				</td>
			</tr>
			<tr style="border:0px;padding:0px;margin:0px;">
				<td style="padding:20px;text-align:center;" colspan="2">
					<p><small>UMUNC</small></p>
				</td>
			</tr>
		</table>
		''')
	# except:
	# 	pass

def sendmail_payment(group):
	for i in group.profile_set.all():
		sendmail_payment_user(i.User)
