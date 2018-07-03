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

bp = Blueprint("top", __name__)

class Top(object):

	__db = None
	__Practice = None
	__CourtName = None
	__CourtType = None

	def __init__(self):
		
		from simpleserver import db
		from model import Practice, CourtName, CourtType

		self.__db = db
		self.__Practice = Practice
		self.__CourtName = CourtName
		self.__CourtType = CourtType

	#最新の練習データを取得
	def get_latest_practice(self, data: dict) -> dict:
		practice = self.__db.session.query(
			self.__Practice.id,
			self.__Practice.title,
			self.__Practice.start_date,
			self.__Practice.start_time,
			self.__Practice.end_date,
			self.__Practice.end_time,
			self.__Practice.dead_date,
			self.__Practice.dead_time,
			self.__Practice.member_num,
			self.__Practice.member_type,
			self.__Practice.court_id
		).order_by(self.__Practice.created_at.desc()).limit(10)

		data['practice'] = []
		for item in practice:
			data['practice'].append({
				'id': item.id,
				'title': item.title,
				'start_date': item.start_date,
				'start_time': item.start_time,
				'end_date': item.end_date,
				'end_time': item.end_time,
				'dead_date': item.dead_date,
				'dead_time': item.dead_time,
				'member_num': item.member_num,
				'member_type': item.member_type,
				'court_id': item.court_id,
			})

		return data


@bp.route('/', methods=['GET'])
def index():

	tp = Top()

	data = {}
	data = tp.get_latest_practice(data)

	return render_template('/main/top/index.html', data=data)