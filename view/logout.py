import sqlite3
from flask import Blueprint, Flask, request, session, g, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from pprint import pprint
from utils import check_database, check_auth
import hashlib

#上のディレクトリをインポートできるようにしておく
import sys
sys.path.append('../')

bp = Blueprint("logout", __name__)

@bp.before_request
def is_login():

	if not check_auth.CheckAuth.is_login():
		return redirect('/login')

class Logout(object):

	def __init__(self):
		pass




@bp.route('/', methods=['GET'])
def index():

	session.pop('mail', None)
	session.pop('password', None)

	data = {}
	return render_template('/main/logout/index.html', data=data)