
from flask import Flask
from pprint import pprint

#データの追加や更新が上手くいっているかチェックする
class CheckDatabase():

	def __init__(self):
		pass

	@classmethod
	#参加申請データの更新が上手くいっているかチェック
	def is_entry_updated_correctly(cls, db, Entry, practice_id: int, member_id: int, condition_id: int):

		if practice_id is None or practice_id == 0: return False
		if member_id is None or member_id == 0: return False

		entry = db.session.query(
			Entry.condition_id
		).filter(
			Entry.practice_id == practice_id
		).filter(
			Entry.member_id == member_id
		).all()

		#指定したcondition_idの値と同じかどうかで判断
		for item in entry:
			return condition_id == item[0]

	@classmethod
	#参加申請データの追加が上手くいっているかチェック
	def is_entry_added_correctly(cls, db, Entry, practice_id: int, member_id: int) -> bool:

		if practice_id is None or practice_id == 0: return False
		if member_id is None or member_id == 0: return False

		entry = db.session.query(
			Entry.condition_id
		).filter(
			Entry.practice_id == practice_id
		).filter(
			Entry.member_id == member_id
		).first()

		return not entry is None

	@classmethod
	#メンバー一時テーブルへの追加が上手くいっているかチェック
	def is_member_tmp_added_correctly(cls, db, MemberTmp, mail: str, token: str, password: str) -> bool:

		if mail is None or mail == '': return False
		if token is None or token == '': return False
		if password is None or password == '': return False

		member_tmp = db.session.query(
			MemberTmp.id
		).filter(
			MemberTmp.mail == mail
		).filter(
			MemberTmp.token == token
		).filter(
			MemberTmp.password == password
		).first()

		pprint(member_tmp)
		return not member_tmp == () and not member_tmp is None

	@classmethod
	#メンバーテーブルへの追加が上手くいっているかチェック
	def is_member_added_correctly(cls, db, Member, name: str, mail: str, password: str) -> bool:

		if name is None or name == '': return False
		if mail is None or mail == '': return False
		if password is None or password == '': return False

		member = db.session.query(
			Member.id
		).filter(
			Member.name == name
		).filter(
			Member.mail == mail
		).filter(
			Member.password == password
		).first()

		return not member == () and not member is None
