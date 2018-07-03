import sqlite3
from flask import Blueprint, Flask, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("meetup", __name__)

@bp.route('/<int:practice_id>')
def meetup(practice_id):

	from simpleserver import db
	from model import Practice, CourtType, CourtName

	if not isinstance(practice_id, int) or practice_id == 0: return "test"
	practice = db.session.query(
			Practice.id,
			Practice.title,
			Practice.start_date,
			Practice.start_time,
			Practice.end_date,
			Practice.end_time,
			Practice.dead_date,
			Practice.dead_time,
			Practice.member_num,
			Practice.member_type,
			CourtName.name.label('court_name'),
			#Practice.court_id,
			CourtType.name.label('court_type'),
			#Practice.court_type,
			Practice.court_num,
			Practice.explain,
			Practice.other
		).join(
			CourtType, Practice.court_type == CourtType.type_id
		).join(
			CourtName, Practice.court_id == CourtName.id
		).filter(
			Practice.id == practice_id
		).all()

	pprint(practice)

	data = {}
	for item in practice:

		data.update({
			'id': item.id,
			'title': item.title,
			'start_date': item.start_date,
			'start_time': item.start_time,
			'end_date': item.end_date,
			'end_time': item.end_time,
			'dead_date': item.dead_date,
			'dead_time': item.dead_time,
			'member_num': item.member_num,
			'member_type': item.member_type,
			'court_name': item.court_name,
			'court_type': item.court_type,
			'court_num': item.court_num,
			'explain': item.explain,
			'other': item.other
		})

	return render_template('/main/meetup/index.html', data=data)