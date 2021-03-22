import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import rueng
from flask import render_template
from flask import request,redirect,url_for
from app import App
from flask_login import current_user,login_required
from pprint import pprint
app = App()
db = app.get_db()
@rueng.route('/',methods=['POST','GET'])
@login_required
def add():
	if request.method == "POST":
		from .models import RuEng,User
		id = current_user.id

		user = User.query.filter(User.id.contains(id)).first()
		w = RuEng(ru=request.form['ru'],eng=request.form['eng'])
		w.users.append(user)
		current_db_sessions = db.session.object_session(w)
		current_db_sessions.add(w)
		current_db_sessions.commit()
		# w.users.append(user)
		print(w)
		return redirect(url_for('rueng.add'))
	return render_template('add.html',current_user=current_user)


@rueng.route('/all')
@login_required
def all():
	from .models import RuEng
	id = current_user.id
	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	print(allw)
	return render_template('all.html',current_user=current_user,allw=allw)

@rueng.route('/all<word_id>')
def del_word(word_id):
	from .models import RuEng
	user_id = current_user.id
	# print(word_id)
	# pprint(user_id)
	text = r'DELETE FROM word_user WHERE Word_id={user_id} AND user_id={word_id};'.format(user_id=user_id,
																						word_id=word_id
																		)
	db.engine.execute(text)

	w = RuEng.query.filter(RuEng.id == word_id).first()
	current_db_sessions = db.session.object_session(w)
	current_db_sessions.commit()
	allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()

	return render_template('all.html',current_user=current_user,allw=allw)

