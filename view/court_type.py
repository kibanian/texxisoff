import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("court_type", __name__)

@bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rest_api():

	from model import CourtType
	from simpleserver import db
	from utils import validation

	def show_court() -> str:

		court_types = db.session.query(
			CourtType.id,
			CourtType.name
		).all()

		ret = {}
		for item in court_types:
			ret.update({'id': item.id, 'name': item.name})

		return jsonify(result=ret)

	def add_court() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'type_id': 'No type_id',
			'name': 'No name'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'type_id': 'type_id is not numeric'
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		court_type = CourtType(request.json['type_id'], request.json['name'])
		db.session.add(court_type)
		db.session.commit()

		return "Success"

	def edit_court() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'id': 'No ID',
			'name': 'No name'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		numeric_validate = {
			'id': 'ID is not numeric'
		}

		messages = vld.check_json(numeric_validate, 'numeric_check')
		if not messages == []:
			return ','.join(messages)

		court_type = db.session.query(CourtType).filter(CourtType.id==request.json['id']).first()

		court_type.name = request.json['name']

		db.session.commit()

		return "Success"

	def delete_court() -> str:

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

		db.session.query(CourtType).filter(CourtType.id==request.json['id']).delete()

		db.session.commit()

		return "Success"

	if request.method == 'GET': return show_court()
	elif request.method == 'POST': return add_court()
	elif request.method == 'PUT': return edit_court()
	elif request.method == 'DELETE': return delete_court()
	else: return "Set Method"