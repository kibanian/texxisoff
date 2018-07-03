import sqlite3
from flask import Blueprint, Flask, request, render_template, session, jsonify, redirect
import requests
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import validation, check_auth, check_database
import logging

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("entry_ctrl", __name__)

#エントリー管理クラス
class EntryCtrl(object):

	__db = None
	__Practice = None
	__Entry = None
	__CourtName = None
	__Member = None
	__Entry = None
	__practice_id = 0

	__accept_msg = '※参加者を追加しました。'
	__reject_msg = '※参加を拒否しました。'
	__unexpected_error_msg = '※予期せぬエラーが発生しました。'
	__limit_error_msg = '※定員オーバーです。'


	def __init__(self, practice_id):
		from simpleserver import db
		from model import Practice, Entry, CourtName, Member

		self.__db = db
		self.__Practice = Practice
		self.__Entry = Entry
		self.__CourtName = CourtName
		self.__Member = Member
		self.__practice_id = practice_id

		#練習が自分の主催したものか確認
		if not check_auth.CheckAuth.is_my_practice(self.__db, self.__Practice, self.__practice_id, 1):
			return redirect('/')

	#参加決定者
	def get_entry(self) -> list:
		entry = self.__db.session.query(
			self.__Entry.id,
			self.__Entry.practice_id,
			self.__Entry.member_id,
			self.__Member.name,
			self.__Entry.condition_id
		).join(
			self.__Member,
			self.__Entry.member_id == self.__Member.id
		).filter(
			self.__Entry.practice_id == self.__practice_id
		).all()

		data = []
		for item in entry:
			data.append({
				'id': item.id,
				'practice_id': item.practice_id,
				'member_id': item.member_id,
				'name': item.name,
				'condition_id': item.condition_id
			})

		return data

	def get_practice(self) -> dict:
		practice = self.__db.session.query(
			self.__Practice.id,
			self.__Practice.title,
			self.__Practice.start_date,
			self.__Practice.start_time,
			self.__CourtName.name.label('court_name'),
		).join(
			self.__CourtName, self.__Practice.court_id == self.__CourtName.id
		).filter(
			self.__Practice.id == self.__practice_id
		).all()

		data = {}
		for item in practice:
			data.update({
				'id': item.id,
				'title': item.title,
				'start_date': item.start_date,
				'start_time': item.start_time
			})

		return data

	def __update_member(self, member_id: int, condition_id: int):
		entry = self.__db.session.query(
			self.__Entry
		).filter(
			self.__Entry.practice_id == self.__practice_id
		).filter(
			self.__Entry.member_id == member_id
		).first()

		entry.condition_id = condition_id

		self.__db.session.commit()

		return check_database.CheckDatabase.is_entry_updated_correctly(self.__db, self.__Entry, self.__practice_id, member_id, condition_id)



	#参加承認する
	def accept_member(self, member_id: int):
		return self.__update_member(member_id, 2)


	#参加不承認する
	def reject_member(self, member_id: int):
		return self.__update_member(member_id, 3)

	#練習の定員を取得
	def get_member_num(self):
		member_num = self.__db.session.query(
			self.__Practice.member_num
		).filter(
			self.__Practice.id == self.__practice_id
		).first()

		return member_num[0]


	#参加者数を取得
	def get_entry_num(self):
		count = self.__db.session.query(
			self.__Entry.id
		).filter(
			self.__Entry.practice_id == self.__practice_id
		).count()

		return count

	def set_accept_msg(self, data):
		data['error_message'].append(self.__accept_msg)
		return data

	def set_reject_msg(self, data):
		data['error_message'].append(self.__reject_msg)
		return data

	def set_unexpected_error_msg(self, data):
		data['error_message'].append(self.__unexpected_error_msg)
		return data

	def set_limit_error_msg(self, data):
		data['error_message'].append(self.__limit_error_msg)
		return data




@bp.route('/<int:practice_id>', methods=['GET', 'POST'])
def index(practice_id: int):

	if practice_id == 0: return redirect('/')

	entry_ctrl = EntryCtrl(practice_id)

	#参加決定者と参加申請者の一覧を取得
	data = {}

	#参加決定者
	data['entry'] = entry_ctrl.get_entry()


	data['practice'] = entry_ctrl.get_practice()

	pprint(data)

	return render_template('/main/entry_ctrl/index.html', data=data)

@bp.route('/accept/<int:practice_id>/<int:member_id>/', methods=['GET', 'POST'])
#参加承認する
def accept(practice_id: int, member_id: int):

	if practice_id == 0: return redirect('/')
	if member_id == 0: return redirect('/')

	entry_ctrl = EntryCtrl(practice_id)

	#参加者は練習の定員より多くすることはできない
	if entry_ctrl.get_member_num() < entry_ctrl.get_entry_num():
		return entry_ctrl.set_limit_error_msg(data)

	if entry_ctrl.accept_member(member_id):
		return entry_ctrl.set_accept_msg(data)
	else:
		return entry_ctrl.set_unexpected_error_msg(data)

@bp.route('/reject/<int:practice_id>/<int:member_id>/', methods=['GET', 'POST'])
#参加非承認する
def reject(practice_id: int, member_id: int):

	if practice_id == 0: return redirect('/')
	if member_id == 0: return redirect('/')

	entry_ctrl = EntryCtrl(practice_id)

	if entry_ctrl.reject_member(member_id):
		return entry_ctrl.set_reject_msg(data)
	else:
		return entry_ctrl.set_unexpected_error_msg(data)