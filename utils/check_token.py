
from flask import Flask
from pprint import pprint
import random

class CheckToken():

	def __init__(self):
		pass

	@classmethod
	#トークンを取得する
	def get_token(cls, num: int):

		if num is None or num == 0: return ''
		source = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		return "".join([random.choice(source) for i in range(num)])