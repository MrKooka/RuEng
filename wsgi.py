from app import App
from rueng.models import User
app = App()
app.reg_blueprints()
login_manager = app.get_login_manager()

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


if __name__ == '__main__':
	app.get_app().run(debug=True,port=8000)