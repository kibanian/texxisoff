import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import validation

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("entry", __name__)

@bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rest_api():

	from model import Entry
	from simpleserver import db

	def get_entry() -> str:

		entries = db.session.query(
			Entry.id,
			Entry.practice_id,
			Entry.member_id
		).all()

		ret = {}
		for item in entries:
			ret[item.id] = {
				'id': item.id,
				'practice_id': item.practice_id,
				'member_id': item.member_id
			}

		return jsonify(result=ret)

	def add_entry() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'practice_id': 'No practice_id',
			'member_id': 'No member_id'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'practice_id': 'practice_id is not numeric',
			'member_id': 'member_id is not numeric'
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		entry = Entry(request.json['practice_id'], request.json['member_id'])
		db.session.add(entry)
		db.session.commit()

		return "Success"

	def edit_entry() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'id': 'No id',
			'practice_id': 'No practice_id',
			'member_id': 'No member_id'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'id': 'id is not numeric',
			'practice_id': 'practice_id is not numeric',
			'member_id': 'member_id is not numeric'
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		entry = db.session.query(Entry).filter(Entry.id==request.json['id']).first()

		entry.practice_id = request.json['practice_id']
		entry.member_id = request.json['member_id']

		db.session.commit()

		return "Success"

	def delete_entry() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'id': 'No ID'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'id': 'ID is not numeric'
		}

		db.session.query(Entry).filter(Entry.id==request.json['id']).delete()

		db.session.commit()

		return "Success"

	if request.method == 'GET': return get_entry()
	elif request.method == 'POST': return add_entry()
	elif request.method == 'PUT': return edit_entry()
	elif request.method == 'DELETE': return delete_entry()
	else: return "Set Method"