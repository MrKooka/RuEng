
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from datetime import datetime 
from flask_security import UserMixin, RoleMixin

from .routes import App
app = App()
db = app.get_db()

word_user = db.Table('word_user',
					 db.Column('Word_id',db.Integer,db.ForeignKey('user.id')),
					 db.Column('user_id',db.Integer,db.ForeignKey('ru_eng.id')))


class RuEng(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ru = db.Column(db.String(80),nullable=False)
    eng = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime,default = datetime.now())

    users = db.relationship('User', secondary=word_user, backref=db.backref('words',lazy='dynamic'))

    def __repr__(self):
        return 'id:{} Ru:{} Eng: {}'.format(self.id,self.ru,self.eng)


class User(db.Model,UserMixin):
  id = db.Column(db.Integer(),primary_key=True)
  email = db.Column(db.String(100),unique=True)
  telegramid = db.Column(db.String(255))
  password = db.Column(db.String(255))
  username = db.Column(db.String(15))
  active = db.Column(db.Boolean())


  def __init__(self,*args,**kwargs):
  	super(User,self).__init__(*args,**kwargs)

  def __repr__(self):
  	return 'id: {}, name: {}'.format(self.id,self.username)





App.add_model(RuEng.__name__,RuEng)
App.add_model(User.__name__,User)
App.add_model('word_user',word_user)

# login_manager = app.get_login_manager()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
# @login_manager.user_loader
# def user_loader(id):
    # return User.query.filter_by(id=id).first()

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = User.query.filter_by(username=username).first()
#     return user if user else None

