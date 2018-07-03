import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import check_database, check_auth
import hashlib

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("login", __name__)

class Login(object):

	__db = None
	__Member = None
	__no_mail_error_message = '※メールアドレスが入力されていません'
	__no_password_error_mesage = '※パスワードが入力されていません'
	__no_member_error_message = '※メールアドレスかパスワードが間違っています'
	__unexpected_error_message = '※予期せぬエラーが発生しました'


	def __init__(self):
		from simpleserver import db
		from model import Member

		self.__db = db
		self.__Member = Member

	#ハッシュ化されたパスワードを取得
	def __get_hashed_password(self, password: str) -> str:
		if password is None or password == '': return None
		return hashlib.sha224(password.encode('utf-8')).hexdigest()

	def __set_error_msg(self, data: dict, msg: str) -> dict:
		pprint(msg)
		if 'error_message' not in data: data['error_message'] = []
		data['error_message'].append(msg)
		return data

	def set_no_mail_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__no_mail_error_msg)

	def set_no_password_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__no_password_error_msg)

	def set_no_member_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__no_member_error_message)

	def set_unexpected_error_msg(self, data) -> dict:
		return self.__set_error_msg(data, self.__unexpected_error_msg)

	#入力されたメールとパスワードが正しいか確認
	def is_member(self, mail, password) -> bool:

		#ハッシュ化されたパスワードを取得する
		hashed_password = self.__get_hashed_password(password)

		if hashed_password is None: return False
		pprint(hashed_password)
		member = self.__db.session.query(
			self.__Member.id
		).filter(
			self.__Member.mail == mail
		).filter(
			self.__Member.password == hashed_password
		).first()

		return not member == () and not member is None

	#ログイン用のセッション追加
	def set_login_session(self, mail, password):
		hashed_password = self.__get_hashed_password(password)

		#キーエラー出さないように、初期化しておく
		session['mail'] = ''
		session['password'] = ''

		if hashed_password is None: return False

		session['mail'] = mail
		session['password'] = hashed_password

		#セッションに格納されているか確認
		return session.get('mail') and session.get('password')


@bp.before_request
def is_login():

	if check_auth.CheckAuth.is_login():
		return redirect('/')



@bp.route('/', methods=['GET', 'POST'])
def index():

	if request.method == 'GET':
		data = {}
		return render_template('/main/login/index.html', data=data)

	elif request.method == 'POST':

		lg = Login()
		data = {}

		mail = request.form['mail']
		password = request.form['password']

		while True:
			if mail is None or mail == '':
				lg.set_no_mail_error_msg(data)
				break
			if password is None or password == '':
				lg.set_no_password_error_msg(data)
				break
			#メールとパスワードのペアを確認
			if not lg.is_member(mail, password):
				lg.set_no_member_error_msg(data)
				break

			#セッションに登録
			if lg.set_login_session(mail, password):
				return redirect('/login/complete')
			else:
				break

		return render_template('/main/login/index.html', data=data)

@bp.route('/complete', methods=['GET'])
def complete():

	lg = Login()
	data = {}

	#セッションに登録されていなければ、トップにリダイレクト
	if not check_auth.CheckAuth.is_login(): return redirect('/')

	return render_template('/main/login/complete.html', data=data)