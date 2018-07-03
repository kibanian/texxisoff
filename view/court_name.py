import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
import requests
import json
from time import sleep

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("court_name", __name__)

#Google Map Apiにアクセスするクラス
class GoogleMap():


	__db = None
	__CourtName = None
	__Pref = None
	__api_key = 'AIzaSyCVITQlBrCJIosRxkX_b_qB_dgMhJ12pNQ'
	__url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
	__language = 'ja'
	__tennis_court = 'テニスコート'

	def __init__(self):
		from model import CourtName, City
		from simpleserver import db

		self.__db = db
		self.__CourtName = CourtName
		self.__City = City

	def __get_cities(self) -> dict:

		data = self.__db.session.query(
			self.__City.pref_name,
			self.__City.city_name
		).all()

		#{県名：[市区名, 市区名, 市区名, ...]}という形式に変更する
		pref = None

		cities = {}
		tmp = []
		for item in data:
			if pref == item.pref_name:
				tmp.append(item.city_name)
			else:
				cities[pref] = tmp
				#変数リセット
				pref = item.pref_name
				tmp = []

		return cities

	#既に保存されているデータかどうか確認する
	def __is_saved_data(self, google_id: str) -> bool:
		count = self.__db.session.query(self.__CourtName).filter(self.__CourtName.google_id==google_id).count()

		return count > 0

	def __access_api(self, query: dict) -> dict:
		r = requests.get(self.__url, params=query)
		r.encoing = 'Shift_JIS'
		return r.json()

	def __insert_data(self, data: dict) -> bool:

		if data is None: return False

		for item in data['results']:
			pprint(item)
			#すでに存在する場合は登録しない
			if self.__is_saved_data(item['id']):
				continue

			court_name = self.__CourtName(
				item['name'],
				item['geometry']['location']['lat'],
				item['geometry']['location']['lng'],
				item['id']
			)
			self.__db.session.add(court_name)
			self.__db.session.commit()

		return True


	def main(self) -> dict:

		#一応バリデーション
		#if district is None: return False

		cities = self.__get_cities()

		#for pref, city_list in self.__cities.items():
		for pref, city_list in cities.items():
			for city in city_list:
				query = {
					#"query": self.__keyword_1+'+'+district,
					"query": '+'.join([pref, city, self.__tennis_court]),
					"key": self.__api_key,
					"language": self.__language
				}

				data = {}
				data = self.__access_api(query)

				if not data == {}:
					self.__insert_data(data)

				sleep(1)



		return "Success"

@bp.route('/googlemap/', methods=['GET'])
def get_info():

	gm = GoogleMap()
	gm.main()

	return ""



@bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rest_api():

	from model import CourtName
	from simpleserver import db
	from utils import validation

	def show_court() -> str:

		court_names = db.session.query(
			CourtName.id,
			CourtName.name
		).all()
		ret = []
		for item in court_names:
			ret.append({'id': item.id,'name': item.name})

		return jsonify(result=ret)

	def add_court() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'name': 'No name',
			'type_id': 'No type_id',
			'lat': 'No lat',
			'lng': 'No lng',
			'google_id': 'No google_id'
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

		court_name = CourtName(
			request.json['name'],
			request.json['name'],
			request.json['type_id'],
			request.json['lat'],
			request.json['lng'],
			request.json['google_id']
		)

		db.session.add(court_name)
		db.session.commit()

		return "Success"

	def edit_court() -> str:

		#バリデーションクラス
		vld = validation.Validation()

		none_validate = {
			'name': 'No name',
			'type_id': 'No type_id',
			'lat': 'No lat',
			'lng': 'No lng',
			'google_id': 'No google_id'
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

		court_name = db.session.query(CourtName).filter(CourtName.id==request.json['id']).first()

		court_name.name = request.json['name']
		court_name.type_id = request.json['type_id']
		court_name.lat = request.json['lat']
		court_name.lng = request.json['lng']
		court_name.google_id = request['google_id']

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