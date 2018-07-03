
from flask import Flask, session
from pprint import pprint
import datetime

#練習データの取得や整形
class PracticeUtils():

	def __init__(self):
		pass

	@classmethod
	#トップページ用の練習データ取得
	def get_latest_practice(cls) -> list:

		from simpleserver import db
		from model import Practice, CourtName, Entry
		#締め切り日時までの残り時間
		def get_rest_time(dead_date, dead_time) -> dict:

			#日付・時刻の形式が正しいかチェック
			if not dead_date.count('-') == 2: return {}
			if not dead_time.count(':') == 2: return {}

			[d_year, d_month, d_date] = dead_date.split('-')
			[d_hour, d_minute, d_second] = dead_time.split(':')

			rest_time = datetime.datetime(d_year, d_month, d_date, d_hour, d_minute, d_second) - datetime.datetime.now()

			return {
				'day': rest_time.days,
				'hour': rest_time.hours,
				'minute': rest_time.minutes
			}

		#残り人数を取得
		def get_rest_num(member_num) -> int:

			#各練習のエントリー数を取得
			def get_entry_num(practice_ids: list) -> list:

				entry = db.session.query(
					Entry.id,
					Entry.practice_id
				).filter(
					Entry.id.in_(practice_ids)
				).group_by(
					Emtry.practice_id
				)

				data = []
				for item in entry:
					data.append({
						practice_id: item.practice_id,
						count: len(item.id)
					})



		practice = db.session.query(
			Practice.title,
			Practice.start_date,
			Practice.start_time,
			Practice.end_date,
			Practice.end_time,
			Practice.dead_date,
			Practice.dead_time,
			Practice.member_num,
			Practice.unit,
			CourtName.name
		).join(
			CourtName,
			CourtName.id == Practice.court_id
		).order_by(
			Practice.updated_at.desc()
		).limit(10).all()

		data = []
		for item in practice:

			#締め切りまで残り日数
			rest_time = get_rest_time(start_date, start_time)
			if rest_time == {}: continue

			#締め切りまで残り人数
			rest_num = get_rest_num(member_num)

			data.append({
				'rest_time':

			})

