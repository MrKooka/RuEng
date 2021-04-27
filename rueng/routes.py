import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import rueng
from flask import render_template,current_app
from flask import request,redirect,url_for,session
from app import db
from flask_login import current_user,login_required
from pprint import pprint
from sqlalchemy.orm import scoped_session, sessionmaker
from random import choice
import ast
from .train import Train
from forms import Add_word
import logging
debug_logger = logging.getLogger('debug_logger')

# with rueng.test_request_context():
# 	# print(current_user.id)
# user_id = 
# train = Train(user_id)
@rueng.route('/common',methods=['POST','GET'])
def common():
	from models import RuEng
	from models import Common

	if not current_user.is_authenticated:
		allw = Common.query.all()
		return render_template('rueng/example.html',allw=allw,choice=choice)

	id= current_user.id
	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	return render_template('rueng/example.html',allw=allw)

	# if request.method =='POST':
		# print(allw)
		# w = Common(ru=request.form['ru'].lower(),eng=request.form['eng'].lower(),context=form.context.data)
		# print(w)
		# db.session.add(w)
		# db.session.commit()
		# return render_template('rueng/example.html',form=form,allw=allw)
	# return render_template('rueng/example.html',allw=allw)


@rueng.route('/',methods=['POST','GET'])
@login_required
def add():
	
	form = Add_word()
	from models import RuEng,User

	id= current_user.id

	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	print(allw)
	if request.method == "POST":

		user = User.query.filter(User.id.contains(id)).first()
		w = RuEng(ru=form.ru.data.lower(),eng=form.eng.data.lower(),context=form.context.data)
		w.users.append(user)
		current_db_sessions = db.session.object_session(w)
		current_db_sessions.add(w)
		current_db_sessions.commit()

		return redirect(url_for('rueng.add'))
	return render_template('rueng/add.html',current_user=current_user,allw=allw,form=form)


@rueng.route('/all')
@login_required
def all():
	form = Add_word()
	from models import RuEng
	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	id = current_user.id

	return render_template('rueng/all.html',current_user=current_user,allw=allw,form=form)

@rueng.route('/all<word_id>')
def del_word(word_id):
	form = Add_word()
	from models import RuEng
	user_id = current_user.id
	sql = r'DELETE FROM word_user WHERE Word_id={user_id} AND user_id={word_id};'.format(user_id=user_id,
																						word_id=word_id,form=form
																		)
	db.engine.execute(sql)

	try:
		w = RuEng.query.filter(RuEng.id == word_id).first()
		current_db_sessions = db.session.object_session(w)
		current_db_sessions.commit()
	except:
		logging.exception('Cant commit db before delete word ')
	allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()
	

	return render_template('rueng/add.html',current_user=current_user,allw=allw,form=form)

@rueng.route('/random')
def random():
	from models import Common

	if not current_user.is_authenticated:
		allw = Common.query.all()
		return render_template('rueng/random.html',err=False,choice=choice,allw=allw)

	user_id = current_user.id
	train = Train(user_id)
	allw = train.get_list_words()
	if len(allw) > 0:
		return render_template('rueng/random.html',err=False,user_id=user_id,choice=choice,allw=allw)
	else:
		return render_template('rueng/random.html',err=True)

# @rueng.route('/random/next_word/')
# def next_word():
# 	user_id = current_user.id
# 	train = Train(user_id)
# 	print('Вывод train',train.get_next_word())
	# return render_template('rueng/random.html',word=word)
	# if len(allw) > 0:
		# allw = allw.pop(allw.index(choice(allw)))
# 		# w = choice(allw)
		# return render_template('rueng/write.html',w=allw,err=False)
	# else:
		# return render_template('rueng/write.html',err=True)

@rueng.route('/write')
def write():
	from models import Common
	if not current_user.is_authenticated:
		allw = Common.query.all()
		return render_template('rueng/write.html',err=False,choice=choice,allw=allw)
	user_id = current_user.id
	train = Train(user_id)
	allw = train.get_list_words()
	if len(allw) > 0:
		return render_template('rueng/write.html',err=False,user_id=user_id,choice=choice,allw=allw)
	else:
		return render_template('rueng/write.html',err=True)



@rueng.route('/write/<eng>',methods=['GET','POST'])
def check_word(eng):
	from models import Common

	if not current_user.is_authenticated:
		allw = Common.query.all()

		if request.method == 'POST':
			if Common.query.filter_by(eng=eng).first().ru == request.form['ru']:
				return render_template('rueng/write.html',allw=allw ,choice=choice,alert='Правильно')
			else:			
				allw = Common.query.filter_by(eng=eng).all() 
				return render_template('rueng/write.html',allw=allw ,choice=choice,alert='Неправильно')

		return render_template('RuEngeng/write.html',allw=allw,err=False,choice=choice)
						
	user_id = current_user.id
	train = Train(user_id)

	if request.method == 'POST':

		if train.check_word(eng,request.form['ru']):
			allw = train.get_list_words()
			
			return render_template('rueng/write.html',allw=allw ,choice=choice,alert='Правильно')
		
		else:
			allw = train.get_list_words(eng)
			return render_template('rueng/write.html',allw=allw ,choice=choice,alert='Неправильно')
 
	return render_template('RuEngeng/write.html',allw=allw,err=False,choice=choice)
