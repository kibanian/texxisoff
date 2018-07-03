
from flask import Flask
from datetime import datetime
from collections import OrderedDict
import requests
from pprint import pprint

#年月データなど、フォームに出すデータを作る
class Formdata():

	__db = None
	__CourtName = None
	__CourtType = None
	__undecided_num = '99'
	__undecided_str = '未定'

	__member_type_list = [
		{'num': '1', 'member_type': '人'},
		{'num': '2', 'member_type': 'ペア'},
		{'num': '3', 'member_type': 'チーム'},
	]

	__title = {}
	__year = {}
	__month = {}
	__date = {}
	__hour = {}
	__minute = {}
	__length = {}
	__deaddate = {}
	__deadtime = {}
	__member_num = {}
	__unit = {}
	__court = {}
	__court_num = {}
	__court_type = {}
	__explain = {}
	__other = {}
	__recommend = {}

	def __init__(self):
		#上のディレクトリをインポートできるようにしておく
		import sys
		sys.path.append('../')
		from simpleserver import db
		from model import CourtName, CourtType

		self.__db = db
		self.__CourtName = CourtName
		self.__CourtType = CourtType

	#タイトルの部品
	def get_title(self) -> dict:
		self.__title = {
			'tag_type': 'text',
			'name': 'title',
			'value': '',
			'id': 'title',
			'size': 40,
			'maxlength': 40,
			'placeholder': '（例）みんなで４時間テニス',
			'is_required': True
		}
		return self.__title

	#年の一覧
	def get_year(self) -> dict:
		self.__year = {
			'tag_type': 'select',
			'name': 'year',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(0, 10):
			self.__year['data'].append({
				'optgroup': '',
				'value': str(datetime.now().year+num),
				'string': str(datetime.now().year+num)
			})

		return self.__year

	#月の一覧
	def get_month(self) -> dict:
		self.__month = {
			'tag_type': 'select',
			'name': 'month',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 13):
			self.__month['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__month['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__month

	#日の一覧
	def get_date(self) -> dict:
		self.__date = {
			'tag_type': 'select',
			'name': 'date',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 32):
			self.__date['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__date['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__date

	#時間の一覧
	def get_hour(self) -> dict:
		self.__hour = {
			'tag_type': 'select',
			'name': 'hour',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 25):
			self.__hour['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__hour['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__hour

	#分の一覧
	def get_minute(self) -> dict:
		self.__minute = {
			'tag_type': 'select',
			'name': 'minute',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in [0, 30]:
			self.__minute['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__minute['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__minute

	#プレー時間の一覧
	def get_length(self) -> dict:
		self.__length = {
			'tag_type': 'select',
			'name': 'length',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 6):
			self.__length['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__length['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__length

	#申し込み締め切り日の一覧
	def get_deaddate(self) -> dict:
		self.__deaddate = {
			'tag_type': 'select',
			'name': 'deaddate',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in [1, 2]:
			self.__deaddate['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)+'日前'
			})

		return self.__deaddate

	#申し込み締切り時刻の一覧
	def get_deadtime(self) -> dict:
		self.__deadtime = {
			'tag_type': 'select',
			'name': 'deadtime',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(20, 24):
			self.__deadtime['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)+'時ごろ'
			})

		self.__deadtime['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__deadtime

	#募集定員数
	def get_member_num(self) -> dict:
		self.__member_num = {
			'tag_type': 'select',
			'name': 'member_num',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 5):
			self.__member_num['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)
			})

		self.__member_num['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})
		return self.__member_num

	#募集単位
	def get_member_type(self) -> dict:
		self.__member_type = {
			'tag_type': 'select',
			'name': 'member_type',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for item in self.__member_type_list:
			self.__member_type['data'].append({
				'optgroup': '',
				'value': item['num'],
				'string': item['member_type']
			})
		return self.__member_type

	#テニスコート
	def get_court(self) -> dict:
		self.__court = {
			'tag_type': 'select',
			'name': 'court_id',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		court_names = self.__db.session.query(
			self.__CourtName.id,
			self.__CourtName.name
		).all()
		for item in court_names:
			self.__court['data'].append({
				'optgroup': '',
				'value': str(item.id),
				'string': item.name
			})
		return self.__court

	#テニスコート面数
	def get_court_num(self) -> dict:
		self.__court_num = {
			'tag_type': 'select',
			'name': 'court_num',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		for num in range(1, 4):
			self.__court_num['data'].append({
				'optgroup': '',
				'value': str(num),
				'string': str(num)+'面'
			})

		self.__court_num['data'].append({
			'optgroup': '',
			'value': self.__undecided_num,
			'string':self.__undecided_str
		})

		pprint(self.__court_num)
		return self.__court_num

	#テニスコート種類
	def get_court_type(self) -> dict:
		self.__court_type = {
			'tag_type': 'select',
			'name': 'court_type',
			'data': [],
			'first_is_empty': True,
			'is_required': True
		}
		court_types = self.__db.session.query(
			self.__CourtType.id,
			self.__CourtType.name
		).all()

		for item in court_types:
			self.__court_type['data'].append({
				'optgroup': '',
				'value': str(item.id),
				'string': item.name
			})
		return self.__court_type

	#概要
	def get_explain(self) -> dict:
		self.__explain = {
			'tag_type': 'textarea',
			'name': 'explain',
			'id': 'explain',
			'cols': 60,
			'maxlength': 300,
			'rows': 5,
			'placeholder': '（例）みんなでわいわいテニスしましょう。',
			'is_required': True
		}
		return self.__explain

	#備考
	def get_other(self) -> dict:
		self.__other = {
			'tag_type': 'textarea',
			'name': 'other',
			'id': 'other',
			'cols': 60,
			'maxlength': 180,
			'rows': 3,
			'placeholder': None,
			'is_required': False
		}
		return self.__other

	#主催者推薦枠
	def get_recommend(self) -> dict:
		self.__recommend = {
			'tag_type': 'text',
			'name': 'recommend[]',
			'value': '',
			'id': None,
			'size': 10,
			'maxlength': None,
			'placeholder': None,
			'is_required': False
		}
		return self.__recommend