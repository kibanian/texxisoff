import sqlite3
from flask import Blueprint, Flask, request, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from validate_email import validate_email
import socket
import hashlib
from utils import check_token, check_database, send_mail



#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("create_member", __name__)

class CreateMember(object):

	__db = None
	__Member = None
	__MemberTmp = None
	__no_mail_error_msg = '※メールアドレスを入力してください'
	__double_mail_error_msg = '※すでに登録されているメールアドレスです'
	__invalid_mail_error_msg = '※メールアドレスの形式が不正です'
	__invalid_host_error_msg = '※使われていないドメインのメールアドレスです'
	__unexpected_error_msg = '※予期せぬエラーが発生しました'
	__invalid_token_error_msg = '※URLに異常があります'

	__member_tmp = None
	__hash_obj = None

	def __init__(self):
		from simpleserver import db
		from model import Member, MemberTmp

		self.__db = db
		self.__Member = Member
		self.__MemberTmp = MemberTmp

	#メールアドレスを分解してホスト名を取得
	def get_host_from_mail(self, mail: str) -> str:
		tmp = mail.split('@')

		return tmp[1]

	#すでに登録されているメールアドレスか確認する
	def is_double_member(self, token: str):
		data = self.__get_member_tmp(token)

		member = self.__db.session.query(
			self.__Member.id
		).filter(
			self.__Member.name == data['name'],
			self.__Member.mail == data['mail'],
			self.__Member.password == data['password']
		).first()

		return not member == () and not member is None




	#すでに登録されているメールアドレスか確認する
	def is_double_member_tmp(self, mail: str) -> bool:
		member_tmp = self.__db.session.query(
			self.__Member.id
		).filter(
			self.__Member.mail == mail
		).first()

		return not member_tmp == () and not member_tmp is None


	#トークンを取得
	def get_token(self) -> str:
		return check_token.CheckToken.get_token(30)

	#パスワードを取得
	def get_password(self) -> str:
		return check_token.CheckToken.get_token(8)
		
	#パスワードをハッシュ化
	def __create_password_hash(self, password: str) -> str:
		if password is None or password == '': return None
		return hashlib.sha224(password.encode('utf-8')).hexdigest()

	#メンバー一時テーブルに登録
	def regist_member_tmp(self, name: str, mail: str, token: str, password: str) -> bool:

		#パスワードをハッシュ化する
		hashed_password = self.__create_password_hash(password)

		if hashed_password is None: return False

		pprint(hashed_password)
		data = self.__MemberTmp(
			mail,
			token,
			hashed_password,
			name
		)

		self.__db.session.add(data)
		self.__db.session.commit()

		#一時メンバーの登録がうまくいったかどうかチェック
		return check_database.CheckDatabase.is_member_tmp_added_correctly(self.__db, self.__MemberTmp, mail, token, hashed_password)

	def __get_member_tmp(self, token: str) -> dict:
		if self.__member_tmp is None or self.__member_tmp == {} or not self.__member_tmp['token'] == token:
			data = self.__db.session.query(
				self.__MemberTmp.name,
				self.__MemberTmp.mail,
				self.__MemberTmp.password,
				self.__MemberTmp.token
			).filter(
				self.__MemberTmp.token == token
			).all()

			self.__member_tmp = {}
			for item in data:
				self.__member_tmp['name'] = item[0]
				self.__member_tmp['mail'] = item[1]
				self.__member_tmp['password'] = item[2]
				self.__member_tmp['token'] = item[3]

			return self.__member_tmp
		else:
			return self.__member_tmp

	#本登録処理
	def regist_member(self, token: str) -> bool:
		data = self.__get_member_tmp(token)

		member = self.__Member(
			data['name'],
			data['mail'],
			data['password']
		)

		self.__db.session.add(member)
		self.__db.session.commit()

		return check_database.CheckDatabase.is_member_added_correctly(self.__db, self.__Member, data['name'], data['mail'], data['password'])


	def __set_error_msg(self, data: dict, msg: str) -> dict:
		pprint(msg)
		if 'error_message' not in data: data['error_message'] = []
		data['error_message'].append(msg)
		return data

	def set_no_mail_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__no_mail_error_msg)

	def set_invalid_mail_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__invalid_mail_error_msg)

	def set_double_mail_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__double_mail_error_msg)

	def set_invalid_host_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__invalid_host_error_msg)

	def set_unexpected_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__unexpected_error_msg)

	def set_invalid_token_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__invalid_token_error_msg)
	 
class MailError(Exception):
	pass


@bp.route('/', methods=['GET', 'POST'])
def create_member():

	if request.method == 'GET':

		data = {}
		return render_template('/main/create_member/index.html', data=data)

	elif request.method == 'POST':

		cm = CreateMember()
		data = {}

		name = request.form['name']

		if name is None or name == '': return False

		mail = request.form['mail']

		while True:
			#メールアドレスとしておかしくないか確認する
			if mail is None:
				data = cm.set_no_mail_error_msg(data)
				break


			#メールアドレス形式チェック
			if not validate_email(mail):
				data = cm.set_invalid_mail_error_msg(data)
				break

			#メールアドレス二重登録チェック
			if cm.is_double_member_tmp(mail):
				data = cm.set_double_mail_error_msg(data)
				break

			#メールアドレスのドメインが有効かチェック
			if not socket.gethostbyname_ex(cm.get_host_from_mail(mail)):
				data = cm.set_invalid_host_error_msg(data)
				break

			#トークン用のランダム文字列を取得
			token = cm.get_token()
			if token == '':
				data = cm.set_unexpected_error_msg(data)
				break

			#パスワード用のランダム文字列を取得
			password = cm.get_password()
			if password == '':
				data = cm.set_unexpected_error_msg(data)
				break

			#メンバー一時テーブルに追加
			if not cm.regist_member_tmp(name, mail, token, password):
				data = cm.set_unexpected_error_msg(data)
				break

			#メールを送信する
			if not send_mail.SendMail.member_tmp_mail(name, mail, token, password):
				data = cm.set_unexpected_error_msg(data)
				break

			return redirect('/create_member/send')

		return render_template('/main/create_member/index.html', data=data)

		
			
			
@bp.route('/send', methods=['GET'])
def send_member():

	data = {}

	return render_template('/main/create_member/send.html', data=data)

@bp.route('complete/<token>', methods=['GET'])
#本登録の処理
def complete_member(token: str):

	cm = CreateMember()
	data = {}

	if token is None:
		data = cm.set_invalid_token_error_msg(data)
		session['error_message'] = data['error_message']
		return redirect('/create_member/fail')

	#すでにメンバー登録済の場合
	if cm.is_double_member(token):
		data = cm.set_double_mail_error_msg(data)
		session['error_message'] = data['error_message']
		return redirect('/create_member/fail')

	if cm.regist_member(token):

		return render_template('/main/create_member/complete.html', data=data)
	else:
		data = cm.set_unexpected_error_msg(data)
		session['error_message'] = data['error_message']

		return redirect('/create_member/fail')

@bp.route('/fail', methods=['GET'])
def fail():
	data = {}
	data['error_message'] = session.get('error_message')

	pprint(data)
	return render_template('/main/create_member/fail.html', data=data)