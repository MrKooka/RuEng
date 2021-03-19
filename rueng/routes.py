import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import rueng
from flask import render_template
from flask import request,redirect,url_for
from app import App
from flask_login import current_user,login_required
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
	allw = RuEng.query.all()
	return render_template('all.html',allw=allw,current_user=current_user)
@rueng.route('/all<w_u>')
def del_word(w_u):
	Word_id,user_id = w_u 
	sql = 'DELETE FROM word_user WHERE Word_id=1 AND user_id =1;'

	RuEng.query.filter(RuEng.eng.contains(w)).first()
