from simpleserver import db




class Practice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(40))
	start_date = db.Column(db.String(10))
	start_time = db.Column(db.String(8))
	end_date = db.Column(db.String(10))
	end_time = db.Column(db.String(8))
	dead_date = db.Column(db.String(10))
	dead_time = db.Column(db.String(8))
	member_num = db.Column(db.Integer)
	member_type = db.Column(db.Integer)
	court_id = db.Column(db.Integer, db.ForeignKey('court_name.id'))
	court_type = db.Column(db.Integer, db.ForeignKey('court_type.type_id'))
	court_num = db.Column(db.Integer)
	explain = db.Column(db.Text)
	other = db.Column(db.Text)
	created_at = db.Column(db.Text)
	updated_at = db.Column(db.Text)
	member_id = db.Column(db.Integer) #主催者のID

	def __init__(self, title, start_date, start_time, end_date, end_time, dead_date, dead_time, member_num, member_type, court_id, court_type, court_num, explain, other, created_at, updated_at, member_id):
		self.title = title
		self.start_date = start_date
		self.start_time = start_time
		self.end_date = end_date
		self.end_time = end_time
		self.dead_date = dead_date
		self.dead_time = dead_time
		self.member_num = member_num
		self.member_type = member_type
		self.court_id = court_id
		self.court_type = court_type
		self.court_num = court_num
		self.explain = explain
		self.other = other
		self.created_at = created_at
		self.updated_at = updated_at
		self.member_id = member_id

	def __repr__(self):
		return '<Practice %r>' % self.title


class CourtType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type_id = db.Column(db.Integer)
	name = db.Column(db.String(40))

	def __init__(self, type_id, name):
		self.type_id = type_id
		self.name = name

	def __repr__(self):
		return '<CourtType %r>' % self.title

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40))
	mail = db.Column(db.Text)
	password = db.Column(db.Text)

	def __init__(self, name, mail, password):
		self.name = name
		self.mail = mail
		self.password = password

	def __repr__(self):
		return '<Member %r>' % self.title


#テニスコート
class CourtName(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	#type_id = db.Column(db.Integer)
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	google_id = db.Column(db.Text)

	def __init__(self, name, lat, lng, google_id):
		self.name = name
		#self.type_id = type_id
		self.lat = lat
		self.lng = lng
		self.google_id = google_id

class Favorite(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	practice_id = db.Column(db.Integer)
	member_id = db.Column(db.Integer)

	def __init__(self, practice_id, member_id):
		self.practice_id = practice_id
		self.member_id = member_id

class City(db.Model):
	city_id = db.Column(db.Integer, primary_key=True)
	pref_name = db.Column(db.String(10))
	city_name = db.Column(db.String(10))

	def __init__(self, city_id, pref_name, city_name):
		self.city_id = city_id
		self.pref_name = pref_name
		self.city_name = city_name

#練習参加者
class Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
	#参加者のID
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	#検討中：1、参加：2、キャンセル：3
	condition_id = db.Column(db.Integer)

	def __init__(self, practice_id, member_id, condition_id):
		self.practice_id = practice_id
		self.member_id = member_id
		self.condition_id = condition_id

#練習参加申請者
class Apply(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'))
	#参加申請者のID
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	#検討中：1、キャンセル：2、参加受理：3
	condition_id = db.Column(db.Integer)

	def __init__(self, practice_id, member_id, condition_id):
		self.practice_id = practice_id
		self.member_id = member_id
		self.condition_id = condition_id

#アカウント作成用テーブル
class MemberTmp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	mail = db.Column(db.Text)
	#ランダム文字列
	token = db.Column(db.Text)
	password = db.Column(db.Text)
	name = db.Column(db.String(10))

	def __init__(self, mail, token, password, name):
		self.mail = mail
		self.token = token
		self.password = password
		self.name = name