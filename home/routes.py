from . import home
from flask import render_template
from flask_login import login_user,logout_user,current_user
from pprint import pprint
@home.route('/')
def index():
	pprint(type(current_user.id))
	return render_template('index.html',current_user=current_user)


