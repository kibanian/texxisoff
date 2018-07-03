import sqlite3
from flask import Blueprint, Flask, request, render_template, session, jsonify, redirect
import requests
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import validation, formdata, formbuilder, check_auth
import logging

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("practice_ctrl", __name__)

class PracticeCtrl(object):

	__db = None
	__Practice = None
	__Member = None


	def __init__(self):
		from simpleserver import db
		from model import Practice, Member

		self.__db = db
		self.__Practice = Practice
		self.__Member = Member

	def get_my_practice(self, data) -> dict:

		mail = session.get('mail')
		password = session.get('password')


		practice = self.__db.session.query(
			self.__Practice.id,
			self.__Practice.title
		).join(
			self.__Member, self.__Member.id == self.__Practice.member_id
		).filter(
			self.__Member.mail == mail
		).filter(
			self.__Member.password == password
		).all()


		data['practice'] = []

		if practice is None: return data

		for item in practice:
			data['practice'].append({
				'id': item.id,
				'title': item.title
			})

		return data

	def __get_member_id(self) -> int:
		data = self.__db.session.query(
			self.__Member.id
		).filter(
			self.__Member.mail == session.get('mail'),
			self.__Member.password == session.get('password')
		).first()

		return data[0]

	def fix_request(self, data) -> dict:


		def join_time(glue: str, strs: list) -> str:
			return glue.join(strs)

		data['title'] = session.get('title')
		start_datetime = datetime.datetime(
			int(session.get('year')),
			int(session.get('month')),
			int(session.get('date')),
			int(session.get('hour')),
			int(session.get('minute'))
		)

		end_datetime = start_datetime + datetime.timedelta(hours=int(session.get('length')))

		dead_datetime = (start_datetime - datetime.timedelta(days=int(session.get('deaddate'))))

		data['start_date'] = join_time('-', [
			(str)(start_datetime.year),
			(str)(start_datetime.month),
			(str)(start_datetime.day)
		])
		data['start_time'] = join_time(':', [
			(str)(start_datetime.hour),
			(str)(start_datetime.minute),
			'00'
		])
		data['end_date'] = join_time('-', [
			(str)(end_datetime.year),
			(str)(end_datetime.month),
			(str)(end_datetime.day)
		])
		data['end_time'] = join_time(':', [
			(str)(end_datetime.hour),
			(str)(end_datetime.minute),
			'00'
		])
		data['dead_date'] = join_time('-', [
			(str)(dead_datetime.year),
			(str)(dead_datetime.month),
			(str)(dead_datetime.day)
		])

		data['dead_time'] = session.get('deadtime')
		data['member_num'] = session.get('member_num')
		data['member_type'] = session.get('member_type')
		data['court_id'] = session.get('court_id')
		data['court_type'] = session.get('court_type')
		data['court_num'] = session.get('court_num')
		data['explain'] = session.get('explain')
		data['other'] = session.get('other')

		return data

	def insert_practice(self, data) -> bool:

		pprint(data)

		practice = self.__Practice(
			data['title'],
			data['start_date'],
			data['start_time'],
			data['end_date'],
			data['end_time'],
			data['dead_date'],
			data['dead_time'],
			data['member_num'],
			data['member_type'],
			data['court_id'],
			data['court_num'],
			data['court_type'],
			data['explain'],
			data['other'],
			datetime.datetime.now(),
			datetime.datetime.now(),
			self.__get_member_id()
		)
		self.__db.session.add(practice)
		self.__db.session.commit()

		return True


 
@bp.before_request
def is_login():
	if not check_auth.CheckAuth.is_login():
		return redirect('/login')

@bp.route('/', methods=['GET'])
def index():

	pc = PracticeCtrl()

	data = {}

	data = pc.get_my_practice(data)

	return render_template('/main/practice_ctrl/index.html', data=data)




@bp.route('/add_practice', methods=['GET', 'POST'])
def add_practice():

	from simpleserver import db
	from model import Practice

	#年月データなどフォームに必要な部品を用意
	def get_dict() -> dict:

		def make_box(fmb, formdata: dict) -> str:
			if formdata['tag_type'] == 'text':
				return fmb.make_text_box(
					formdata['name'],
					formdata['value'],
					formdata['id'],
					formdata['size'],
					formdata['maxlength'],
					formdata['placeholder'],
					formdata['is_required']
				)
			elif formdata['tag_type'] == 'select':
				return fmb.make_select_box(
					formdata['name'],
					formdata['data'],
					formdata['first_is_empty'],
					formdata['is_required']
				)
			elif formdata['tag_type'] == 'textarea':
				return fmb.make_textarea(
					formdata['name'],
					formdata['id'],
					formdata['cols'],
					formdata['maxlength'],
					formdata['rows'],
					formdata['placeholder'],
					formdata['is_required']
				)

		#フォームデータクラス
		fmd = formdata.Formdata()
		#フォームビルダークラス
		fmb = formbuilder.FormBuilder()
		data = {}

		data['title'] = make_box(fmb, fmd.get_title())
		data['year'] = make_box(fmb, fmd.get_year())
		data['month'] = make_box(fmb, fmd.get_month())
		data['date'] = make_box(fmb, fmd.get_date())
		data['hour'] = make_box(fmb, fmd.get_hour())
		data['minute'] = make_box(fmb, fmd.get_minute())
		data['length'] = make_box(fmb, fmd.get_length())
		data['deaddate'] = make_box(fmb, fmd.get_deaddate())
		data['deadtime'] = make_box(fmb, fmd.get_deadtime())
		data['member_num'] = make_box(fmb, fmd.get_member_num())
		data['member_type'] = make_box(fmb, fmd.get_member_type())
		data['court'] = make_box(fmb, fmd.get_court())
		data['court_num'] = make_box(fmb, fmd.get_court_num())
		data['court_type'] = make_box(fmb, fmd.get_court_type())
		data['explain'] = make_box(fmb, fmd.get_explain())
		data['other'] = make_box(fmb, fmd.get_other())
		data['recommend'] = make_box(fmb, fmd.get_recommend())

		pprint(data)

		return data

	if request.method == 'GET':
		return render_template('main/practice_ctrl/add.html', data=get_dict())
	elif request.method == 'POST':

		name_list = [
			'title',
			'year',
			'month',
			'date',
			'hour',
			'minute',
			'length',
			'deaddate',
			'deadtime',
			'member_num',
			'member_type',
			'court_id',
			'court_num',
			'court_type',
			'explain',
			'other'
		]

		for item in name_list:
			session[item] = request.form[item]

		return redirect('/practice_ctrl/confirm_practice', code=301)

@bp.route('/confirm_practice', methods=['GET', 'POST'])
def confirm_practice():

	if request.method == 'GET':
		data = {}

		data['title'] = session.get('title')
		data['year'] = session.get('year')
		data['month'] = session.get('month')
		data['date'] = session.get('date')
		data['hour'] = session.get('hour')
		data['minute'] = session.get('minute')
		data['length'] = session.get('length')
		data['deaddate'] = session.get('deaddate')
		data['deadtime'] = session.get('deadtime')
		data['member_num'] = session.get('member_num')
		data['member_type'] = session.get('member_type')
		data['court'] = session.get('court_id')
		data['court_num'] = session.get('court_num')
		data['court_type'] = session.get('court_type')
		data['explain'] = session.get('explain')
		data['other'] = session.get('other')
		#data['recommend'] = session.get('recommend')

		return render_template('main/practice_ctrl/confirm.html', data=data)

	elif request.method == 'POST':

		pc = PracticeCtrl()

		data = {}
		data = pc.fix_request(data)

		#DBに登録
		pc.insert_practice(data)

		return redirect('/practice_ctrl/complete_practice')

@bp.route('/complete_practice', methods=['GET', 'POST'])
def complete_practice():

	
	#セッション削除
	session.pop('title', None)
	session.pop('year', None)
	session.pop('month', None)
	session.pop('date', None)
	session.pop('hour', None)
	session.pop('minute', None)
	session.pop('length', None)
	session.pop('deaddate', None)
	session.pop('deadtime', None)
	session.pop('member_num', None)
	session.pop('member_type', None)
	session.pop('court_id', None)
	session.pop('court_num', None)
	session.pop('court_type', None)
	session.pop('explain', None)
	session.pop('other', None)

	data = {}

	return render_template('/main/practice_ctrl/complete.html', data=data)