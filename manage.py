from app import *
from models import *

manager = app.migrate()

if __name__ == '__main__':
	manager.run()