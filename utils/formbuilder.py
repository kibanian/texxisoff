
from flask import Flask
from pprint import pprint

#フォームの部品を作成する
class FormBuilder():

	def __init__(self):
		pass

	#セレクトボックス
	def make_select_box(self, name: str, data: dict, first_is_empty: bool, is_required: bool) -> str:

		#selectタグを作成
		def make_select_tag(name: str, is_required: bool) -> list:
			if is_required:
				return ['<select name="'+name+'" required >', '</select>']
			else:
				return ['<select name="'+name+'" >', '</select>']

		#optionタグ作成、optgroupタグがある場合は、optgroupタグで囲む
		def make_option_tag(data: dict) -> list:

			#指定したoptgroupのデータだけ抽出
			def select_data(data: dict, optgroup: str) -> dict:
				tmp_data = {}
				for item in data:
					if optgroup == item['optgroup']:
						tmp_data.update(item)

				return tmp_data

			def make_optgroup_tag(data: dict) -> dict:
				#ひとつでもoptgroupの設定ない要素があればoptgroupつけない
				for item in data:
					if item['optgroup'] == '' or item['optgroup'] is None:
						return None

				#optgroupの種類だけ、optgroupタグを用意する
				tag = []
				optgroup = ''
				for item in data:
					if optgroup != item['optgroup']:
						optgroup = item['optgroup']
						tag.append({'optgroup': optgroup, 'tag':['<optgroup label="'+optgroup+'" >', '</optgroup>']})

				return tag

			#optionタグを生成する部分を共通化
			def get_tag(data: dict, html: list, first_is_empty: bool) -> str:
				if first_is_empty:
					html.append('<option value="" ></option>')
				for item2 in data:
					if not isinstance(item2['value'], str): continue
					html.append('<option value="'+item2['value']+'" >'+item2['string']+'</option>')

				return html


			tag = []
			html = []

			tag = make_optgroup_tag(data)

			if tag is None or tag == []:
				html = get_tag(data, html, first_is_empty)
			else:
				for item in tag:
					html.append(item['tag'][0])
					html = get_tag(select_data(data, item['optgroup']), html, first_is_empty)
					html.append(item['tag'][1])


			return html

		#リストのデータをjoin関数で文字列にする
		def join_loop(data: list) -> str:
			html = ''

			for item in data:
				#要素がリストの場合、再帰的に実行
				if isinstance(item, list): html += join_loop(item)
				else: html += item

			return html

		#引数name、引数dictは必須のため
		if name is None or not isinstance(name, str) or name == '': return False
		if data is None or not isinstance(data, list) or data == []: return False

		html = []
		#selectタグを作成
		#[select, [optgroup, opt, opt, ..., optgroup], select]の形式にする
		html = make_select_tag(name, is_required)
		html.insert(1, make_option_tag(data))

		return join_loop(html)

	#テキストボックス
	def make_text_box(self, name: str, value: str, id_str: str, size: int, maxlength: int, placeholder: str, is_required: bool) -> str:

		#引数name、引数valueは必須のため
		if name is None or not isinstance(name, str) or name == '': return False
		if value is None or not isinstance(value, str): return False

		html = []
		html.append('<input type="text"')
		html.append('name="'+name+'"')
		html.append('value="'+value+'"')

		if not id_str is None and not id_str == '':
			html.append('id="'+id_str+'"')
		if not size is None and not size == 0:
			html.append('size="'+str(size)+'"')
		if not maxlength is None and not maxlength == 0:
			html.append('maxlength="'+str(maxlength)+'"')
		if not placeholder is None and not placeholder == '':
			html.append('placeholder="'+placeholder+'"')
		if is_required:
			html.append('required')

		html.append('>')
		return ' '.join(html)

	#テキストエリア
	def make_textarea(self, name: str, id_str: str, cols: int, maxlength: int, rows: int, placeholder: str, is_required: bool) -> str:

		#引数name、引数cols、引数rowsは必須のため
		if name is None or not isinstance(name, str) or name == '': return False
		if cols is None or not isinstance(cols, int) or cols == 0: return False
		if rows is None or not isinstance(rows, int) or rows == 0: return False

		html = []
		html.append('<textarea ')
		html.append('name="'+name+'"')
		html.append('cols="'+str(cols)+'"')
		html.append('rows="'+str(rows)+'"')

		if not id_str is None and not id_str == '':
			html.append('id="'+id_str+'"')
		if not maxlength is None and not maxlength == 0:
			html.append('maxlength="'+str(maxlength)+'"')
		if not placeholder is None and not placeholder == '':
			html.append('placeholder="'+placeholder+'"')
		if is_required:
			html.append('required')

		html.append('></textarea>')

		return ' '.join(html)