from app import App
app = App()
app.register_blueprints()

if __name__ == '__main__':
	app.get_app().run(debug=True,port=8000)