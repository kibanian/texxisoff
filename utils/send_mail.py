
from flask import Flask
from pprint import pprint
import smtplib
from email.mime.text import MIMEText




class SendMail():

	__from_address = 'yourmailaddress'

	def __init__(self):
		pass

	@classmethod
	#仮登録メールを送る
	def member_tmp_mail(cls, name, mail, token, password):

		#メール送信がうまくいったらTrue
		try:
			text = "Hi "+name+".\n\n\nThis is provisional registration. Please access this URL.\nhttp://54326.s.time4vps.cloud/create_member/complete/"+token+"\nYour password is "+password+" at first. Please change password immediately."
			msg = MIMEText(text)
			msg['Subject'] = "Texxis off like site."
			msg['From'] = cls.__from_address
			msg['To'] = mail

			s = smtplib.SMTP()
			s.connect()
			s.sendmail(cls.__from_address, [mail], msg.as_string())
			s.close()

		except Exception as e:
			print(e)
			return False

		return True