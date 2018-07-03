import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
from pprint import pprint
from cerberus import Validator

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("member", __name__)

@bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rest_api():

	from model import Member
	from simpleserver import db
	from utils import validation

	def show_member() -> str:

		members = db.session.query(
			Member.id,
			Member.name,
			Member.mail,
			Member.password
		).all()

		ret = {}
		for item in members:
			ret[item.id] ={
				'id': item.id,
				'name': item.name,
				'mail': item.mail,
			}

		return jsonify(result=ret)

	def add_member() -> str:

		vld = validation.Validation()

		none_validate = {
			'name': 'No name',
			'mail': 'No mail',
			'password': 'No password'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		vld = Validator({
			'name': {
				'type': 'string',
				'required': True,
				'empty': False,
				'maxlength': 40
			},
			'mail': {
				'type': 'string',
				'required': True,
				'empty': False,
				'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
			},
			'password': {
				'type': 'string',
				'required': True,
				'empty': False,
				'regex': '\A(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,30}\Z(?i)'
			}
		})

		messages = vld.validate({
			'name': request.json['name'],
			'mail': request.json['mail'],
			'password': request.json['password']
		})

		if messages == True: pass
		elif not messages == {}:
			pprint(messages)
			#return ','.join(messages)
			return "error"

		name = request.json['name']
		mail = request.json['mail']
		password = request.json['password']

		member = Member(name, mail, password)
		db.session.add(member)
		db.session.commit()

		return "Success"

	def edit_member() -> str:

		vld = validation.Validation()

		none_validate = {
			'name': 'No name',
			'mail': 'No mail',
			'password': 'No password'
		}

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		vld = Validator({
			'id': {
				'type': 'integer',
				'required': True,
				'empty': False,
			},
			'name': {
				'type': 'string',
				'required': True,
				'empty': False,
				'maxlength': 40
			},
			'mail': {
				'type': 'string',
				'required': True,
				'empty': False,
				'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
			},
			'password': {
				'type': 'string',
				'required': True,
				'empty': False,
				'regex': '\A(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,30}\Z(?i)'
			}
		})

		messages = vld.validate({
			'id': request.json['id'],
			'name': request.json['name'],
			'mail': request.json['mail'],
			'password': request.json['password']
		})

		if messages == True: pass
		elif not messages == {}:
			pprint(messages)
			#return ','.join(messages)
			return "error"

		member = db.session.query(Member).filter(Member.id==request.json['id']).first()
		member.name = request.json['name']
		member.mail = request.json['mail']
		member.password = request.json['password']
		db.session.commit()

		return "Success"

	def delete_member() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = { 'id':'No ID' }

		messages = vld.check_json(none_validate, 'null_check')
		if not messages == []:
			return ','.join(messages)

		vld = Validator({
			'id': {
				'type': 'integer',
				'required': True,
				'empty': False,
			}
		})

		messages = vld.validate({
			'id': request.json['id']
		})

		if messages == True: pass
		elif not messages == {}:
			pprint(messages)
			#return ','.join(messages)
			return "error"

		db.session.query(Member).filter(Member.id==request.json['id']).delete()

		db.session.commit()

		return "Success"

	if request.method == 'GET': return show_member()
	elif request.method == 'POST': return add_member()
	elif request.method == 'PUT': return edit_member()
	elif request.method == 'DELETE': return delete_member()
	else: return "Set Method"