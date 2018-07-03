import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
import logging

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("practice", __name__)

@bp.route('/', methods=['GET','POST', 'PUT', 'DELETE'])
def rest_api():

	from model import Practice, CourtType
	from simpleserver import db
	from utils import validation

	def join_time(glue: str, strs: list) -> str:
		return glue.join(strs)

	def fix_request() -> tuple:
		title = request.json['title']
		start_datetime = datetime.datetime(
			int(request.json['year']),
			int(request.json['month']),
			int(request.json['date']),
			int(request.json['hour']),
			int(request.json['minute'])
		)

		end_datetime = start_datetime + datetime.timedelta(hours=int(request.json['length']))

		dead_datetime = (start_datetime - datetime.timedelta(days=int(request.json['deaddate'])))

		start_date = join_time('-', [
			(str)(start_datetime.year),
			(str)(start_datetime.month),
			(str)(start_datetime.day)
		])
		start_time = join_time(':', [
			(str)(start_datetime.hour),
			(str)(start_datetime.minute),
			'00'
		])
		end_date = join_time('-', [
			(str)(end_datetime.year),
			(str)(end_datetime.month),
			(str)(end_datetime.day)
		])
		end_time = join_time(':', [
			(str)(end_datetime.hour),
			(str)(end_datetime.minute),
			'00'
		])
		dead_date = join_time('-', [
			(str)(dead_datetime.year),
			(str)(dead_datetime.month),
			(str)(dead_datetime.day)
		])
		dead_time = request.json['deadtime']
		member_num = request.json['membernum']
		member_type = request.json['membertype']
		court_id = request.json['courtid']
		court_type = request.json['courttype']
		court_num = request.json['courtnum']
		explain = request.json['explain']
		other = request.json['other']

		return (title, start_date, start_time, end_date, end_time, dead_date, dead_time, member_num, member_type, court_id, court_type, court_num, explain, other)

	def show_practices() -> str:
		practices = db.session.query(
			Practice.title,
			Practice.start_date,
			Practice.start_time,
			Practice.end_date,
			Practice.end_time,
			Practice.dead_date,
			Practice.dead_time,
			Practice.member_num,
			Practice.member_type,
			Practice.court_id,
			CourtType.name.label('court_type'),
			#Practice.court_type,
			Practice.court_num,
			Practice.explain,
			Practice.other
		).join(
			CourtType, Practice.court_type == CourtType.type_id
		).all()

		if practices is None:
			return {}

		ret = {}
		for item in practices:
			ret.update({
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
				'court_type': item.court_type,
				'court_num': item.court_num,
				'explain': item.explain,
				'other': item.other
			})

		return jsonify(result=ret)

	def add_practice() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		#JSON形式で値が入っているかチェック
		none_validate = {
			'title':'No Title',
			'year' : 'No Year',
			'month' : 'No Month',
			'date' : 'No Date',
			'hour' : 'No Hour',
			'minute' : 'No Minute',
			'length' : 'No Length',
			'deaddate' : 'No Deaddate',
			'deadtime' : 'No Deadtime',
			'membernum' : 'No Membernum',
			'membertype' : 'No Membertype',
			'courtid' : 'No Courtid',
			'courttype' : 'No Courttype',
			'courtnum' : 'No Courtnum',
			'explain' : 'No Explain',
			'other' : 'No Other',
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'year': 'Year is not numeric',
			'month': 'Month is not numeric',
			'hour': 'Hour is not numeric',
			'date': 'Date is not numeric',
			'length': 'Length is not numeric',
			'deaddate' : 'Deaddate is not numeric',
			'deadtime' : 'Deadtime is not numeric',
			'membernum' : 'Membernum is not numeric',
			'membertype' : 'Membertype is not numeric',
			'courttype' : 'Courttype is not numeric',
			'courtnum' : 'Courtnum is not numeric',
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not message == []:
			return ','.join(messages)

		title, start_date, start_time, end_date, end_time, dead_date, dead_time, member_num, member_type, court_id, court_type, explain, other = fix_request()

		practice = Practice(title, start_date, start_time, end_date, end_time, dead_date, dead_time, member_num, member_type, court_id, court_num, court_type, explain, other)
		db.session.add(practice)
		db.session.commit()

		return 'Success'

	def edit_practice() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'id':'No ID',
			'title':'No Title',
			'year' : 'No Year',
			'month' : 'No Month',
			'date' : 'No Date',
			'hour' : 'No Hour',
			'minute' : 'No Minute',
			'length' : 'No Length',
			'deaddate' : 'No Deaddate',
			'deadtime' : 'No Deadtime',
			'membernum' : 'No Membernum',
			'membertype' : 'No Membertype',
			'courtid' : 'No Courtid',
			'courttype' : 'No Courttype',
			'courtnum' : 'No Courtnum',
			'explain' : 'No Explain',
			'other' : 'No Other',
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'id': 'ID is not numeric',
			'year': 'Year is not numeric',
			'month': 'Month is not numeric',
			'hour': 'Hour is not numeric',
			'date': 'Date is not numeric',
			'length': 'Length is not numeric',
			'deaddate' : 'Deaddate is not numeric',
			'deadtime' : 'Deadtime is not numeric',
			'membernum' : 'Membernum is not numeric',
			'membertype' : 'Membertype is not numeric',
			'courttype' : 'Courttype is not numeric',
			'courtnum' : 'Courtnum is not numeric',
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		practice = db.session.query(Practice).filter(Practice.id==request.json['id']).first()

		title, start_date, start_time, end_date, end_time, dead_date, dead_time, member_num, member_type, court_id, court_type, court_num, explain, other = fix_request()

		practice.title = title
		practice.start_date = start_date
		practice.start_time = start_time
		practice.end_date = end_date
		practice.end_time = end_time
		practice.dead_date = dead_date
		practice.dead_time = dead_time
		practice.member_num = member_num
		practice.member_type = member_type
		practice.court_id = court_id
		practice.court_type = court_type
		practice.court_num = court_num
		practice.explain = explain
		practice.other = other

		db.session.commit()

		return "Success"

	def delete_practice() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = { 'id':'No ID' }

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = { 'id': 'ID is not numeric' }

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		db.session.query(Practice).filter(Practice.id==request.json['id']).delete()

		db.session.commit()

		return "Success"

	logging.basicConfig(level=logging.DEBUG)


	if request.method == 'GET': return show_practices()
	elif request.method == 'POST': return add_practice()
	elif request.method == 'PUT': return edit_practice()
	elif request.method == 'DELETE': return delete_practice()
	else:
		return "Set Method"