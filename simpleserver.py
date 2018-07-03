import sys
import sqlite3
from flask import Blueprint, Flask
import datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from view import practice, court_type, member, entry, court_name, apply_practice, meetup, create_member, login, logout, top
from admin_view import practice_ctrl, entry_ctrl

app = Flask(__name__)

app.secret_key = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/renshu.db'
db = SQLAlchemy(app)


app.register_blueprint(top.bp, url_prefix='/')

app.register_blueprint(login.bp, url_prefix='/login')
app.register_blueprint(logout.bp, url_prefix='/logout')

app.register_blueprint(practice.bp, url_prefix='/practice')
app.register_blueprint(court_type.bp, url_prefix='/court_type')
app.register_blueprint(member.bp, url_prefix='/member')
app.register_blueprint(entry.bp, url_prefix='/entry')
app.register_blueprint(court_name.bp, url_prefix='/court_name')

app.register_blueprint(apply_practice.bp, url_prefix='/apply')
app.register_blueprint(meetup.bp, url_prefix='/meetup')

app.register_blueprint(create_member.bp, url_prefix='/create_member')

app.register_blueprint(apply_practice.bp, url_prefix='/apply_practice')
app.register_blueprint(practice_ctrl.bp, url_prefix='/practice_ctrl')
app.register_blueprint(entry_ctrl.bp, url_prefix='/entry_ctrl')

if __name__ == "__main__":
	app.run(debug=True)