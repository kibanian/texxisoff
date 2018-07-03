import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import check_database, check_auth

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("apply_practice", __name__)

class MeetUp(object):

	__db = None
	__Practice = None
	__Entry = None
	__practice_id = 0
	__double_entry_error_msg = '※すでに参加申請済みです。'
	__entry_failed_error_msg = '※参加申請に失敗しました。もう一度参加申請してください。'
	__dead_line_error_msg = '※すでに応募の期限を過ぎています。'

	def __init__(self, practice_id: int):
		from simpleserver import db
		from model import Practice, Entry

		self.__db = db
		self.__Practice = Practice
		self.__Entry = Entry
		self.__practice_id = practice_id

	def set_index_data(self) -> dict:
		#練習データを載せる
		practice = self.__db.session.query(
			self.__Practice.id,
			self.__Practice.title,
			self.__Practice.start_date,
			self.__Practice.start_time,

		).filter(
			self.__Practice.id == self.__practice_id
		).all()

		data = {}
		for item in practice:
			data['id'] = item.id
			data['title'] = item.title
			data['start_date'] = item.start_date
			data['start_time'] = item.start_time

		#ログイン中のユーザーの情報を渡す
		data['member_id'] = '2'

		#エラーメッセージ用の要素
		data['error_message'] = []

		return data

	#エントリー
	def add_entry(self):
		data = self.__Entry(
			session.get('id'),
			session.get('member_id'),
			'1'
		)

		self.__db.session.add(data)
		self.__db.session.commit()

		#エントリーがうまくいっているか確認
		return check_database.CheckDatabase.is_entry_added_correctly(self.__db, self.__Entry, session.get('id'), session.get('member_id'))

	#二重登録の防止
	def check_double_apply(self) -> bool:
			check = self.__db.session.query(
				self.__Entry.id
			).filter(
				self.__Entry.practice_id == session.get('id')
			).filter(
				self.__Entry.member_id == session.get('member_id')
			).all()

			return not check == []

	#練習の申し込み締切日時を過ぎているか確認する
	def check_deadline(self) -> bool:

		def set_deadline(date: str, time: str):
			date_list = date.split('-')
			time_list = date.split(':')

			return datetime.datetime(
				date_list[0],
				date_list[1],
				date_list[2],
				time_list[0],
				time_list[1],
				time_list[2]
			)

		deadline = self.__db.session.query(
			self.__Practice.dead_date,
			self.__Practice.dead_time
		).filter(
			self.__Practice.id == self.__practice_id
		).first()

		tmp_data = {}
		for item in deadline:
			tmp_data['date'] = item[0]
			tmp_data['time'] = item[1]

		#形式のエラーがないか確認
		if tmp_data['date'] is None or tmp_data['date'] == '': return False
		if not tmp_data['date'].count('-') == 2: return False
		if tmp_data['time'] is None or tmp_data['time'] == '': return False
		if not tmp_data['date'].count(':') == 2: return False

		return datetime.datetime.now() > set_deadline(tmp_data['date'], tmp_data['time'])


	#練習が募集打ち切りになっているか確認
	def check_closing(self) -> bool:
		pass

	def set_double_entry_error(self, data: dict) -> dict:
		data['error_message'].append(self.__double_entry_error_msg)
		return data

	def set_entry_failed_error(self, data: dict) -> dict:
		data['error_message'].append(self.__entry_failed_error_msg)
		return data

	def set_dead_line_error(self, data: dict) -> dict:
		data['error_message'].append(self.__dead_line_error_msg)
		return data

	#セッションを初期化
	def init_session(self):
		session['id'] = None
		session['member_id'] = None

	#セッションに情報をセット
	def set_session(self, data: dict):
		session['id'] = data['id']
		session['member_id'] = data['member_id']

	#セッションの情報削除
	def unset_session(self, data: dict):
		session.pop('id', None)
		session.pop('member_id', None)

@bp.before_request
def is_login():

	if not check_auth.CheckAuth.is_login():
		return redirect('/login')


@bp.route('/<int:practice_id>', methods=['GET', 'POST'])
def apply_meetup(practice_id):

	meetup = MeetUp(practice_id)

	if request.method == 'GET':

		if practice_id == 0:
			return redirect('/')

		data = {}
		data = meetup.set_index_data()

		#該当するセッションを初期化
		meetup.init_session()

		#セッションにIDなど保存
		meetup.set_session(data)

		return render_template('/main/apply/index.html', data=data)

	elif request.method == 'POST':

		while True:

			data = {}
			#二重登録の場合、申請画面に戻る
			if meetup.check_double_apply():
				data = meetup.set_index_data()
				data = meetup.set_double_entry_error(data)
				break

			#練習の申し込み締め切り日時を過ぎていたら、申請画面に戻る
			if meetup.check_deadline():
				data = meetup.set_index_data()
				data = meetup.set_dead_line_error(data)
				break

			#申請者テーブルに登録
			if meetup.add_entry():
				#問題なければ完了画面へ
				return redirect('/apply/complete')
			else:
				#失敗している場合は、申請画面に戻す
				data = meetup.set_entry_failed_error(data)
				break
				
			return redirect('/apply_practice/complete')
		
		return render_template('/main/apply/index.html', data=data)


@bp.route('/complete', methods=['GET'])
def apply_complete():

	meetup = MeetUp(0)
	#セッションを削除する
	meetup.unset_session()

	return "Completed"