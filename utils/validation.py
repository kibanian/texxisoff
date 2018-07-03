
from flask import Flask, request

class Validation():




	def __init__(self):
		pass

	#バリデーションに引っかかった項目のメッセージを返す
	def check_json(self, check_list: dict, check_type: str) -> list:
		#phpのisset的処理
		def is_set(key) -> bool:
			try:
				return request.json[key]
			#値が無ければメッセージ返す
			except KeyError:
				return False

		def is_numeric(key) -> bool:
			return request.json[key].isnumeric()



		messages = []
		for key, value in check_list.items():
			if check_type == 'null_check' and not is_set(key):
				messages.append(value)
			if check_type == 'numeric_check' and not is_numeric(key):
				messages.append(value)

		return messages

		

