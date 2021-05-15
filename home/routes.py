import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import home
from flask import render_template,session,make_response,request,redirect,url_for,flash
from flask_login import login_user,logout_user,current_user
from pprint import pprint
from models import User,db,RuEng
from sqlalchemy import update
@home.route('/')
def index():
	return render_template('home/index.html',current_user=current_user)

def verifyExt(filename):
	permissible_ext = ['png','PNG','jpeg','JPEG','ico','ICO','webp','WebP','HEIC','helc','jpg','JPG']
	ext = filename.rsplit('.',1)[1]
	if ext in permissible_ext:
		print('раширение файла True')
		return True
	print('раширение файла False')

	return False

def getAvatar():
	from pprint import pprint
	img = None
	img = User.query.filter(User.id == current_user.id).first().avatar
	if not img:
		try:
			with open(home.root_path+'/templates/images/avatar2.png','rb') as f:
				img = f.read()
				return img
		except Exception as e:
			print('Ошибка:',str(e))
		else:
			pass
	return img

@home.route('/profile')
def profile():

	id= current_user.id
	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	count = len(allw)
	return render_template('home/profile.html',allw=allw,count=count)

@home.route('/userava')
def userava():
	img = getAvatar()
	if not img:
		return ''
	h = make_response(img)
	h.headers['Content-Type'] = 'image/png'
	return img
@home.route('/upload',methods=['POST','GET'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file  and verifyExt(file.filename):
			try:
				img = file.read()
				user = User.query.filter(User.id == current_user.id).first()
				user.avatar = img
				# update(User).where(User.id==current_user.id).values(avatar = img)
				db.session.commit()

			except Exception as e:
				print('Ошибка:',str(e))
				return redirect(url_for('home.profile'))
		else:
			flash('Недопустимый формат изображения')
			flash("Пожалуйста используйте форматы 'png','PNG','jpeg','JPEG','ico','ICO','webp','WebP','HEIC','helc'")



			
		return redirect(url_for('home.profile'))
	return render_template('home/profile.html')

