
from flask import Flask, session
from pprint import pprint

#ログイン状態を維持しているかなどチェックする
class CheckAuth():

	def __init__(self):
		pass

	@classmethod
	#練習が自分の主催したものかチェックする
	#練習データに保存しているメンバーIDと突き合わせる
	def is_my_practice(cls, db, Practice, practice_id: int, member_id: int) -> bool:

		if practice_id is None or practice_id == 0: return False
		if member_id is None or member_id == 0: return False

		data = db.session.query(
			Practice.member_id
		).filter(
			Practice.id == practice_id
		).all()

		for item in data:
			return member_id == item[0]

	@classmethod
	#ログイン中かチェックする
	def is_login(cls) -> bool:

		from simpleserver import db
		from model import Member

		mail = session.get('mail')
		password = session.get('password')

		if mail is None or mail == '': return False
		if password is None or password == '': return False

		member = db.session.query(
			Member.id
		).filter(
			Member.mail == mail
		).filter(
			Member.password == password
		).first()
		pprint('is_login')

		return not member == () and not member is None