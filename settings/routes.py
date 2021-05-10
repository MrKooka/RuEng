import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import settings
from flask import redirect,url_for,render_template,request
from forms import RegisterForm_,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user,logout_user,current_user
from pprint import pprint
from flask_login import LoginManager,login_required
from models import User
import logging
debug_logger = logging.getLogger('debug_logger')
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')
@settings.route('/',methods=['POST','GET'])
def signup():
	debug_logger.debug('Enter to signup function')
	form = RegisterForm_()
	if form.validate_on_submit():
		debug_logger.debug('Attempt reguster user')
		user = User.query.filter(User.email == form.email.data).first()
		if user:
			debug_logger.debug('Entered Email already exist email:{}'.format(form.email.data))
			debug_logger.debug('signup закончила работу')
			return render_template('settings/signup.html',form=form,current_user=current_user,alert = 'Такой Email уже занят')
		debug_logger.debug('Attempt reguster user email is not exist')
		try:
			hashed_pass = generate_password_hash(form.password.data,method='sha256')
			new_user = User(email = form.email.data,
						telegramid = form.telegramid.data,
						password =hashed_pass,
						username = form.username.data,
						avatar = None
			)
			db.session.add(new_user)
			db.session.commit()
			app.get_login_manager()
		except:
			logging.exception(f'unsuccessful attempt add new user to database')
		return redirect(url_for('settings.login'))
	return render_template('settings/signup.html',form=form,current_user=current_user)

@settings.route('/login',methods=['POST','GET'])
def login():
	debug_logger.debug('Enter to login function')
	form = LoginForm()
	if request.method=="POST":
		debug_logger.debug('Attempt to login')
		try:
			user = User.query.filter_by(email=form.email.data).first()
		except:
			logging.exception(f'Cant find a user email:{form.email.data}')
		if user:
			try:		
				if check_password_hash(user.password, form.password.data):
					login_user(user, remember=form.remember.data,force=True)
			except:
				logging.exception('Cant start login_user')
			return redirect(url_for('rueng.add'))
		return render_template('settings/login.html',form=form,current_user=current_user,alert='Неправильный пароль или email')
	return render_template('settings/login.html',form=form,current_user=current_user)

@settings.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))